import streamlit as st
import google.generativeai as genai
import smtplib
import random
from email.mime.text import MIMEText
from email.utils import formatdate

# ---------------------------------------------------------
# 1. ブランディング & ページ設定
# ---------------------------------------------------------
LOGO_FILE = "GEMINI_gazou.png" 

st.set_page_config(
    page_title="謝罪DX Ultra", 
    page_icon=LOGO_FILE, 
    layout="centered"
)

# ---------------------------------------------------------
# 2. デザインカスタマイズ (CSS)
# ---------------------------------------------------------
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #0f172a;
        color: #f8fafc;
    }}
    .logo-container {{
        text-align: center;
        padding-bottom: 10px;
        border-bottom: 2px double #D4AF37; 
        margin-bottom: 20px;
    }}
    h1 {{
        color: #D4AF37;
        font-family: 'Georgia', serif;
        font-weight: 900;
        text-align: center;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
    }}
    .stAlert {{
        background-color: #ffffff !important; 
        color: #0f172a !important;           
        border: 3px solid #00ffcc !important; 
        border-radius: 12px;
        font-size: 1.15em;
        line-height: 1.7;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
    }}
    label p {{
        color: #f3e5f5 !important;
        font-weight: bold;
    }}
    .stButton>button {{
        width: 100%;
        border-radius: 30px;
        background: linear-gradient(45deg, #7b1fa2, #00ffcc); 
        color: #0f172a;
        font-weight: 900;
        font-size: 1.2em;
        border: none;
        height: 3.5em;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background: linear-gradient(45deg, #00ffcc, #D4AF37); 
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.7);
        transform: scale(1.02);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ロゴとタイトルの表示 ---
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    try:
        st.image(LOGO_FILE, use_container_width=True)
    except:
        pass

st.markdown('<div class="logo-container"><h1>謝罪DX Ultra</h1></div>', unsafe_allow_html=True)
st.caption("やらかしてももう平気！次世代の謝罪DXソリューションアプリ")

# ---------------------------------------------------------
# 3. システム設定 (Secrets)
# ---------------------------------------------------------
api_key = st.secrets.get("GEMINI_API_KEY", "")
gmail_user = st.secrets.get("GMAIL_USER", "")
gmail_password = st.secrets.get("GMAIL_PASSWORD", "")

# ---------------------------------------------------------
# 4. 入力セクション
# ---------------------------------------------------------
with st.sidebar:
    st.header("🛰️ System Status")
    if api_key and gmail_user:
        st.success("Resilience System: Online")
    else:
        st.error("Setup Incomplete")

col_in1, col_in2 = st.columns(2)
with col_in1:
    my_name = st.text_input("あなたの名前：", placeholder="（例：いしい）")
with col_in2:
    target_name = st.text_input("相手の名前：", placeholder="（例：佐藤部長）")

user_fact = st.text_area("起きてしまった事象：", placeholder="例：デスクにコーヒーをぶちまけてしまった")

mode = st.select_slider(
    "転送強度（他責レベル）：",
    options=["平謝り（リスク低）", "少し言い訳（推奨）", "最強の他責（責任消失）"]
)

# ---------------------------------------------------------
# 5. 生成ロジック（エラー対策版）
# ---------------------------------------------------------
if st.button("謝罪文案の生成（Ultra Build）"):
    if not api_key:
        st.error("APIキーが未設定です")
    elif not user_fact or not target_name:
        st.warning("名前と事象を入力してください")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # ★修正：利用可能なモデルを動的に検索する
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # flashがあれば優先、なければpro、それもなければ取得した最初のモデルを使う
            selected_model = 'models/gemini-1.5-flash' # デフォルト
            if 'models/gemini-1.5-flash' in available_models:
                selected_model = 'models/gemini-1.5-flash'
            elif 'models/gemini-pro' in available_models:
                selected_model = 'models/gemini-pro'
            elif available_models:
                selected_model = available_models[0]
            
            model = genai.GenerativeModel(selected_model)
            
            prompt = f"""
            あなたは世界最高のビジネスマンです。
            以下の情報を元に、適切な謝罪文を作成してください。ただし、強度が「最強の他責」の場合は言い訳をしてください。
            【宛名】: {target_name} / 【差出人】: {my_name} / 【事象】: {user_fact}  /【強度】: {mode}
            
            指令：
            1. 自然な挨拶から開始。
            2. 200文字以内。
            3. ビジネスの口調を遵守。
            """
            
            with st.spinner('謝罪文案を生成中...'):
                response = model.generate_content(prompt)
                st.session_state.result = response.text
                st.session_state.risk = random.randint(0, 100)
                st.success(f"理論構築完了！ (Model: {selected_model})")
        except Exception as e:
            st.error(f"モデル接続エラー: {e}")

# ---------------------------------------------------------
# 6. 表示 & 送信
# ---------------------------------------------------------
if 'result' in st.session_state:
    st.markdown("---")
    st.info(st.session_state.result)
    
    risk = st.session_state.risk
    st.write(f"📊 **リスク分析：クビになる確率 {risk}%**")
    if risk < 30: st.success("判定：セーフ。引き続きお仕事に励みましょう。")
    elif risk < 70: st.warning("判定：注意。怒鳴り声に備えてください。")
    else: st.error("判定：危険。至急、転職活動を開始してください！")

    st.subheader("📩 責任転送（Gmail送信）")
    dest_email = st.text_input("送信先メールアドレス：", placeholder="boss@example.com")
    
    if st.button("この理論を送信（Resilience Transfer）"):
        try:
            sig_name = my_name if my_name else ""
            footer = f"\n\n---\n{sig_name}\nSME Consultant | DX Strategist"
            final_text = f"{st.session_state.result}{footer}"
            
            msg = MIMEText(final_text)
            msg['Subject'] = f"【報告】本日の事象につきまして（{sig_name}）"
            msg['From'] = gmail_user
            msg['To'] = dest_email
            msg['Date'] = formatdate(localtime=True)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(gmail_user, gmail_password)
                smtp.send_message(msg)
            
            st.balloons()
            st.success("送信完了！お疲れさまでした。")
        except Exception as e:
            st.error(f"送信エラー: {e}")

st.markdown("---")
st.caption("開発者: いしいけいすけ (Registered SME Consultant)")
