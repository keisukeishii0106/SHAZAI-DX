import streamlit as st
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

# ---------------------------------------------------------
# 1. デザイン：視認性重視の「プロ仕様」カスタマイズ
# ---------------------------------------------------------
st.set_page_config(page_title="不可抗力DX Pro", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    /* 全体の背景を明るいグレーに */
    .stApp {
        background-color: #f8f9fa;
        color: #212529;
    }
    /* タイトル：深みのあるエメラルドで見やすく */
    h1 {
        color: #00796b;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: 800;
        border-bottom: 2px solid #00796b;
        padding-bottom: 10px;
    }
    /* サブヘッダー */
    h3 {
        color: #495057;
    }
    /* ボタン：押しやすさと高級感を両立 */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #00796b;
        color: white;
        height: 3em;
        font-size: 1.2em;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #004d40;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    /* テキストエリアと入力欄をクッキリさせる */
    textarea, input {
        border: 2px solid #ced4da !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 不可抗力DX Pro")
st.caption("〜 管理企画の英知を集結させた、究極の他責システム 〜")

# Secretsから読み込み
api_key = st.secrets.get("GEMINI_API_KEY", "")
gmail_user = st.secrets.get("GMAIL_USER", "")
gmail_password = st.secrets.get("GMAIL_PASSWORD", "")

# ---------------------------------------------------------
# 2. メインロジック
# ---------------------------------------------------------
with st.sidebar:
    st.header("🛰️ System Status")
    if api_key and gmail_user:
        st.success("All Systems GO")
        st.write(f"User: {gmail_user}")
    else:
        st.error("Setup Incomplete")

st.subheader("1. 現場の「失態」を報告せよ")
user_fact = st.text_area("事実を簡潔に：", placeholder="例：寝坊して会議を飛ばした")

st.subheader("2. 戦略的言い訳モード")
mode = st.select_slider(
    "強度の選択：",
    options=["情緒的謝罪", "論理的不可抗力", "宇宙規模の他責"]
)

# 生成ボタン
if st.button("超理論をビルドする"):
    if not api_key:
        st.error("APIキーがありません")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # 【404対策】動くモデルを自動で探し出す最強ロジック
            model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            target_model = model_list[0] if model_list else 'gemini-pro'
            
            model = genai.GenerativeModel(target_model)
            
            prompt = f"""
            あなたは世界最高の言い訳コンサルタントです。
            以下の「事実」を「{mode}」モードで不可抗力に変換してください。
            【事実】: {user_fact}
            
            【制約】:
            1. 文章は必ず「150文字以内」で完結させること。
            2. 相手が反論できないほど圧倒的な語彙を使うこと。
            3. 極端なまでのビジネス形式にすること。
            """
            
            with st.spinner(f'理論構築中（Using: {target_model}）...'):
                response = model.generate_content(prompt)
                st.session_state.result = response.text
                st.success("理論ビルド成功！")
        except Exception as e:
            st.error(f"Error: {e}")

# 生成結果の表示
if 'result' in st.session_state:
    st.markdown("---")
    st.markdown("### 📄 構築された超理論 (150文字要約)")
    # 見やすいように背景を少し変えたエリアに表示
    st.info(st.session_state.result)

    # ---------------------------------------------------------
    # 3. Gmail連携機能
    # ---------------------------------------------------------
    st.subheader("📩 相手の脳内へ直接送信（他責DX）")
    dest_email = st.text_input("送信先メールアドレス：", placeholder="boss@example.com")
    
    if st.button("この理論をメールで送信"):
        if not gmail_user or not gmail_password:
            st.error("SecretsにGmail設定がありません！")
        elif not dest_email:
            st.warning("送信先を入れてください")
        else:
            try:
                msg = MIMEText(st.session_state.result)
                msg['Subject'] = "【重要】本日の事象に関するご報告"
                msg['From'] = gmail_user
                msg['To'] = dest_email
                msg['Date'] = formatdate(localtime=True)

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(gmail_user, gmail_password)
                    smtp.send_message(msg)
                
                st.balloons()
                st.success(f"無事に {dest_email} へ責任転送を完了しました！")
            except Exception as e:
                st.error(f"メール送信エラー: {e}")

st.markdown("---")
st.caption(f"Logged in as: {gmail_user} | SME Consultant Keisuke Ishii Edition")
