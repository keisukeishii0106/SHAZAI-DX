import streamlit as st
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

# ---------------------------------------------------------
# 1. デザイン：視認性重視の「プロ仕様」
# ---------------------------------------------------------
st.set_page_config(page_title="謝罪DX Pro", page_icon="🙇‍♂️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; color: #212529; }
    h1 { color: #d32f2f; font-family: 'Helvetica Neue', Arial, sans-serif; font-weight: 800; border-bottom: 2px solid #d32f2f; padding-bottom: 10px; }
    h3 { color: #495057; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #d32f2f; color: white; height: 3em; font-size: 1.2em; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #b71c1c; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
    textarea, input { border: 2px solid #ced4da !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🙇‍♂️ 他責思考DX Pro")
st.caption("〜 100%の非を、戦略的不可抗力へ昇華させる 〜")

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
        st.write(f"Logged in: {gmail_user}")
    else:
        st.error("Setup Incomplete")

# ①＆② 名前の入力欄を追加
col1, col2 = st.columns(2)
with col1:
    my_name = st.text_input("あなたの名前：", value="石井")
with col2:
    target_name = st.text_input("相手の名前：", placeholder="志々目部長")

st.subheader("1. 現場の「失態」を報告せよ")
user_fact = st.text_area("事実を簡潔に：", placeholder="例：寝坊して会議をすっぽかした")

st.subheader("2. 戦略的言い訳モード")
mode = st.select_slider(
    "強度の選択：",
    options=["情緒的謝罪", "論理的不可抗力", "宇宙規模の他責"]
)

# 生成ボタン
if st.button("超理論をビルドする"):
    if not api_key:
        st.error("APIキーがありません")
    elif not user_fact or not target_name:
        st.warning("名前と事実を入力してください")
    else:
        try:
            genai.configure(api_key=api_key)
            model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            target_model = model_list[0] if model_list else 'gemini-1.5-flash'
            model = genai.GenerativeModel(target_model)
            
            # ③ 200文字制限 ＆ 名前反映のプロンプト
            prompt = f"""
            あなたは世界最高の言い訳コンサルタントです。
            以下の情報を元に、完璧な「超理論」を作成してください。
            
            【宛名】: {target_name}
            【差出人】: {my_name}
            【やらかした事実】: {user_fact}
            【モード】: {mode}
            
            【制約】:
            1. 文章は必ず「200文字以内」で完結させること。
            2. 冒頭は「{target_name}様、お世話になっております。{my_name}です。」から始めること。
            3. {mode}の特性を活かし、個人の意志では制御不能だったことを論理的に強調すること。
            4. 結論として「今回の件は不可避であった」と相手に納得させること。
            """
            
            with st.spinner(f'理論構築中...'):
                response = model.generate_content(prompt)
                st.session_state.result = response.text
                st.success("理論ビルド成功！")
        except Exception as e:
            st.error(f"Error: {e}")

# 生成結果の表示
if 'result' in st.session_state:
    st.markdown("---")
    st.markdown(f"### 📄 構築された超理論 ({target_name}様 宛)")
    st.info(st.session_state.result)

    # 3. Gmail連携機能
    st.subheader("📩 相手の脳内へ直接送信")
    dest_email = st.text_input("送信先メールアドレス：", placeholder="boss@example.com")
    
    if st.button("この理論をメールで送信"):
        if not gmail_user or not gmail_password:
            st.error("SecretsにGmail設定がありません")
        elif not dest_email:
            st.warning("送信先を入れてください")
        else:
            try:
                msg = MIMEText(st.session_state.result)
                msg['Subject'] = f"【ご報告】本日の事象につきまして（{my_name}）"
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
