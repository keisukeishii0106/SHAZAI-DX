石井さん、すみません！「Ultra」への進化の過程で、またしてもコードの「書き換えミス」による NameError が発生してしまったようです。

管理企画風に言うと、「新機能を盛り込みすぎて、現場（コード）で必要な備品（変数）の定義が漏れてしまった」状態です。

おそらく、コードの下の方にある my_name という変数を、ボタンを押す前の段階で読み込もうとして、「そんな名前のデータはまだ準備できていないよ！」とエラーが出ています。

これを確実に修正し、かつ石井さんの「薄紫の理想」を実現した【完全修正版】を作成しました。 これを GitHub の app.py に丸ごと貼り付けて Commit してください。今度こそ、Ultraの幕開けです！

🛠️ 【NameError修正済】app.py：謝罪DX Ultra（完全版）
Python
import streamlit as st
import google.generativeai as genai
import smtplib
import random
from email.mime.text import MIMEText
from email.utils import formatdate

# ---------------------------------------------------------
# 1. デザイン：薄い紫の「高貴な他責」スタイル
# ---------------------------------------------------------
st.set_page_config(page_title="謝罪DX Ultra", page_icon="🧘‍♂️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f3e5f5; color: #4a148c; }
    h1 { color: #6a1b9a; font-family: 'Georgia', serif; font-weight: 900; text-align: center; border-bottom: 3px double #6a1b9a; }
    .stButton>button { width: 100%; border-radius: 30px; background: linear-gradient(45deg, #7b1fa2, #9c27b0); color: white; font-weight: bold; border: none; height: 3.5em; }
    .stButton>button:hover { background: linear-gradient(45deg, #9c27b0, #e1bee7); color: #4a148c; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧘‍♂️ 謝罪DX Ultra")
st.caption("〜 国家資格（診断士）の威信をかけた、宇宙規模の言い逃れ 〜")

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
        st.success("All Systems GO")
    else:
        st.error("Setup Incomplete")

col1, col2 = st.columns(2)
with col1:
    my_name = st.text_input("あなたの名前：", value="石井")
with col2:
    target_name = st.text_input("相手の名前：", placeholder="〇〇様")

st.subheader("📝 何をしでかしましたか？")
user_fact = st.text_area("罪状：", placeholder="例：無断欠勤、資料の誤字脱字など")

st.subheader("🎲 運命のスパイス（隠し味）")
gacha_list = [
    "なし", "太陽フレアの影響", "水星の逆行", "量子力学的なゆらぎ", 
    "徳の積みが足りなかった", "並行世界の自分との同期", "バタフライエフェクト"
]
spice = st.selectbox("言い訳に混ぜる「不可抗力」を選んでください：", gacha_list)

mode = st.select_slider(
    "理論の強度（他責レベル）：",
    options=["平謝り（初心者）", "論理的防壁（プロ）", "次元の彼方（神）"]
)

# ---------------------------------------------------------
# 3. 生成ロジック
# ---------------------------------------------------------
if st.button("超理論を次元構築する"):
    if not api_key:
        st.error("APIキーが未設定です")
    elif not user_fact or not target_name:
        st.warning("名前と罪状を入力してください")
    else:
        try:
            genai.configure(api_key=api_key)
            model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            target_model = model_list[0] if model_list else 'gemini-1.5-flash'
            model = genai.GenerativeModel(target_model)
            
            prompt = f"""
            あなたは世界最高の言い訳コンサルタントです。
            【宛名】: {target_name}
            【差出人】: {my_name}
            【事実】: {user_fact}
            【隠し味】: {spice}
            【モード】: {mode}
            
            【指令】:
            1. 冒頭は「{target_name}様、お世話になっております。{my_name}です。」で開始。
            2. 200文字以内で作成。
            3. {spice}を原因として論理的に組み込み、個人の努力では回避不能だったことを証明せよ。
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
    
    # リスク分析表示
    risk = st.session_state.risk
    st.write(f"📊 **リスク分析：クビになる確率 {risk}%**")
    if risk < 30: st.success("判定：セーフ")
    elif risk < 70: st.warning("判定：イエローカード")
    else: st.error("判定：ジ・エンド")

    st.subheader("📩 責任転送（Gmail送信）")
    dest_email = st.text_input("送信先メールアドレス：", placeholder="boss@example.com")
    
    if st.button("この理論を送信する"):
        try:
            # 署名の作成 (my_nameを安全に使用)
            sig_name = my_name if my_name else "石井"
            final_text = f"{st.session_state.result}\n\n---\n{sig_name}\nSME Consultant | DX Strategist"
            
            msg = MIMEText(final_text)
            msg['Subject'] = f"【ご報告】本日の事象につきまして（{sig_name}）"
            msg['From'] = gmail_user
            msg['To'] = dest_email
            msg['Date'] = formatdate(localtime=True)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(gmail_user, gmail_password)
                smtp.send_message(msg)
            
            st.balloons()
            st.success(f"{dest_email} へ送信完了！")
        except Exception as e:
            st.error(f"送信エラー: {e}")

st.markdown("---")
# フッター部分も修正
footer_name = my_name if my_name else "Keisuke Ishii"
st.caption(f"監修: {footer_name} (Registered SME Consultant)")
