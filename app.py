import streamlit as st
import google.generativeai as genai
import smtplib
import random
from email.mime.text import MIMEText
from email.utils import formatdate

# ---------------------------------------------------------
# 1. デザイン：高貴なラベンダー（レジリエンス・パープル）
# ---------------------------------------------------------
st.set_page_config(page_title="謝罪DX Ultra", page_icon="🙇‍♂️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f3e5f5; color: #4a148c; }
    h1 { color: #6a1b9a; font-family: 'Helvetica Neue', sans-serif; font-weight: 900; text-align: center; border-bottom: 3px double #6a1b9a; }
    .stButton>button { width: 100%; border-radius: 30px; background: linear-gradient(45deg, #7b1fa2, #9c27b0); color: white; font-weight: bold; border: none; height: 3.5em; }
    .stButton>button:hover { background: linear-gradient(45deg, #9c27b0, #e1bee7); color: #4a148c; }
    </style>
    """, unsafe_allow_html=True)

st.title("🙇‍♂️ 謝罪DX Ultra")
st.caption("個人の過失を量子力学・地磁気・太陽フレアの責任へと戦略的に転送する、次世代の他責化ソリューション。謝罪という非生産的なコストを削減し、日本経済のレジリエンスを言い訳によって強化します。")

# Secrets
api_key = st.secrets.get("GEMINI_API_KEY", "")
gmail_user = st.secrets.get("GMAIL_USER", "")
gmail_password = st.secrets.get("GMAIL_PASSWORD", "")

# ---------------------------------------------------------
# 2. 入力セクション
# ---------------------------------------------------------
with st.sidebar:
    st.header("🛰️ System Status")
    if api_key and gmail_user:
        st.success("Resilience System: Online")
    else:
        st.error("Setup Incomplete")

col1, col2 = st.columns(2)
with col1:
    my_name = st.text_input("あなたの名前：", value="", placeholder="（例：石井）")
with col2:
    target_name = st.text_input("相手の名前：", placeholder="（例：佐藤部長、田中さん）")

st.subheader("📝 戦略的報告が必要な「事象」")
user_fact = st.text_area("罪状：", placeholder="例：デスクにコーヒーをぶちまけてしまった")

st.subheader("🎲 不可抗力の注入（スパイス）")
gacha_list = [
    "なし", "太陽フレアの影響", "地磁気の乱れ", "量子力学的なゆらぎ", 
    "水星の逆行", "徳の積みが足りなかった", "並行世界の自分との同期"
]
spice = st.selectbox("原因として採用する外部要因：", gacha_list)

mode = st.select_slider(
    "転送強度（他責レベル）：",
    options=["平謝り（リスク低）", "論理的防壁（推奨）", "次元の彼方（責任消失）"]
)

# ---------------------------------------------------------
# 3. 生成ロジック
# ---------------------------------------------------------
if st.button("超理論を次元構築する"):
    if not api_key:
        st.error("APIキーが未設定です")
    elif not user_fact or not target_name:
        st.warning("名前と事象を入力してください")
    else:
        try:
            genai.configure(api_key=api_key)
            model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            target_model = model_list[0] if model_list else 'gemini-1.5-flash'
            model = genai.GenerativeModel(target_model)
            
            prompt = f"""
            あなたは世界最高の戦略的言い訳コンサルタントです。
            以下の情報を元に、個人の過失を外部要因へ転送する「超理論」を作成してください。
            
            【宛名】: {target_name}
            【差出人】: {my_name}
            【事象】: {user_fact}
            【外部要因】: {spice}
            【モード】: {mode}
            
            【指令】:
            1. 挨拶：{target_name}との関係性を考慮し、「お世話になっております」または「お疲れ様です」など、最も自然なものを選んで開始すること。
            2. 長さ：200文字以内。
            3. 理論：{spice}を原因として組み込み、「これは個人の努力では回避不能な、日本経済のレジリエンスに関わる事態である」というスタンスで記述すること。
            4. 自分の非を一切認めず、むしろ自分も被害者であるかのように振る舞うこと。
            """
            
            with st.spinner('宇宙の意志を確認中...'):
                response = model.generate_content(prompt)
                st.session_state.result = response.text
                st.session_state.risk = random.randint(0, 100)
                st.success("理論構築完了！")
        except Exception as e:
            st.error(f"Error: {e}")

# ---------------------------------------------------------
# 4. 表示 & 送信
# ---------------------------------------------------------
if 'result' in st.session_state:
    st.markdown("---")
    st.info(st.session_state.result)
    
    risk = st.session_state.risk
    st.write(f"📊 **リスク分析：クビになる確率 {risk}%**")
    if risk < 30: st.success("判定：セーフ。相手の思考が停止しています。")
    elif risk < 70: st.warning("判定：注意。診断士の論理力でねじ伏せてください。")
    else: st.error("判定：危険。至急、転職活動を開始してください。")

    st.subheader("📩 責任転送（Gmail送信）")
    dest_email = st.text_input("送信先メールアドレス：", placeholder="boss@example.com")
    
    if st.button("この理論を送信する"):
        try:
            # 署名の作成 (名前が空ならブランク)
            sig_name = my_name if my_name else ""
            footer = f"\n\n---\n{sig_name}\nSME Consultant | DX Strategist" if sig_name else ""
            final_text = f"{st.session_state.result}{footer}"
            
            msg = MIMEText(final_text)
            msg['Subject'] = f"【戦略的報告】本日の事象につきまして（{sig_name}）"
            msg['From'] = gmail_user
            msg['To'] = dest_email
            msg['Date'] = formatdate(localtime=True)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(gmail_user, gmail_password)
                smtp.send_message(msg)
            
            st.balloons()
            st.success(f"{dest_email} へ送信完了！レジリエンスが強化されました。")
        except Exception as e:
            st.error(f"送信エラー: {e}")

st.markdown("---")
footer_name = my_name if my_name else "Guest User"
st.caption(f"監修: {footer_name} (Registered SME Consultant)")
