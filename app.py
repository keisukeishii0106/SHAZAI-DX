import streamlit as st
import google.generativeai as genai
import random

# 1. ページ設定
st.set_page_config(page_title="謝罪DX Ultra", page_icon="🙇‍♂️", layout="centered")

# 2. 【改善】ボタンの色を「何があっても」固定するCSS
st.markdown("""
    <style>
    .stApp { background-color: #1e1b4b; color: #f8fafc; }
    .centered-logo { display: flex; justify-content: center; margin-bottom: 30px; }
    .centered-logo img { width: 450px !important; }

    /* ボタンの強制着色 (Disabled状態でも色を維持する) */
    div.stButton > button {
        width: 100% !important;
        height: 4em !important;
        border-radius: 12px !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        opacity: 1 !important; /* 透明度を1に固定 */
    }
    
    /* 誠心誠意：青 */
    .sincere-btn div.stButton > button { background-color: #2563eb !important; }
    /* 他責：グラデーション */
    .ultra-btn div.stButton > button { background: linear-gradient(45deg, #7c3aed, #d4af37) !important; }
    
    /* ボタンの中の文字を絶対白にする */
    div.stButton > button p { color: #ffffff !important; font-size: 1.2em !important; }

    .result-card {
        background-color: #ffffff !important; color: #1e1b4b !important;
        border: 4px solid #818cf8; border-radius: 12px; padding: 20px; margin-top: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. コンテンツ描画
st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
try: st.image("GEMINI_gazou.png")
except: st.write("🌌")
st.markdown('</div><h1 style="text-align: center;">謝罪DX Ultra</h1>', unsafe_allow_html=True)

app_mode = st.radio("モード選択：", ["誠心誠意", "他責（Ultra Resilience）"], horizontal=True)
col1, col2 = st.columns(2)
with col1: my_name = st.text_input("あなたの名前：", placeholder="例：いしい")
with col2: target_name = st.text_input("相手の名前：", placeholder="例：佐藤部長")
user_fact = st.text_area("起きてしまった事象：", placeholder="例：デスクにコーヒーをぶちまけてしまった")

# 4. ボタン配置
if app_mode == "誠心誠意":
    st.markdown('<div class="sincere-btn">', unsafe_allow_html=True)
    execute = st.button("謝罪文案の生成")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="ultra-btn">', unsafe_allow_html=True)
    execute = st.button("言い訳をひねり出す")
    st.markdown('</div>', unsafe_allow_html=True)

# 5. 生成ロジック (エラーハンドリング強化)
if execute:
    api_key = st.secrets.get("GEMINI_API_KEY")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        with st.spinner('宇宙の意志を確認中...'):
            response = model.generate_content(f"{user_fact}の謝罪文を作れ")
            st.session_state.result_text = response.text
            st.toast("生成成功！")
    except Exception as e:
        if "429" in str(e):
            st.error("【重要】1日の利用制限(20回)を超えました！")
            st.info("今日は生成しすぎです。明日の夕方まで待つか、別のAPIキーを試してください。")
            # 制限中でも動作確認できるようにダミーを表示
            st.session_state.result_text = "（これはデバッグ用表示です）現在はAPI制限中ですが、UIは正常に動作しています！"
        else:
            st.error(f"エラー: {e}")

if 'result_text' in st.session_state:
    st.markdown(f'<div class="result-card">{st.session_state.result_text}</div>', unsafe_allow_html=True)

st.caption("©開発者：いしいけいすけ(SME Consultant)")
