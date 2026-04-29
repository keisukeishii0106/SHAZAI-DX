import streamlit as st
import google.generativeai as genai
import random

# ---------------------------------------------------------
# 1. ページ設定
# ---------------------------------------------------------
st.set_page_config(page_title="謝罪DX Ultra", page_icon="🙇‍♂️", layout="centered")

if 'sp_points' not in st.session_state:
    st.session_state.sp_points = 0
if 'apology_rank' not in st.session_state:
    st.session_state.apology_rank = "見習い謝罪師"

# ---------------------------------------------------------
# 2. デザイン (モード選択の文字を白くする！)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* 全体背景 */
    .stApp { background-color: #1e1b4b; color: #f8fafc; }
    
    /* ロゴのセンタリング */
    .centered-logo { display: flex; justify-content: center; margin-bottom: 20px; }
    .centered-logo img { width: 450px !important; }

    /* ★モード選択（ラジオボタン）の文字を白く、太くする */
    div[data-testid="stRadio"] label p {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 1.1em !important;
        text-shadow: 1px 1px 2px #000; /* 読みやすくするための影 */
    }
    
    /* 入力欄のラベル（あなたの名前：等）も白く */
    .stTextInput label, .stTextArea label, div[data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
        font-weight: bold !important;
    }

    /* ボタンの強制色付け（何があっても白くさせない） */
    div.stButton > button {
        width: 100% !important;
        height: 4em !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        display: block !important;
    }

    .sincere-btn div.stButton > button { background-color: #2563eb !important; }
    .ultra-btn div.stButton > button { background: linear-gradient(45deg, #7c3aed, #d4af37) !important; }
    
    /* ボタンの中の文字 */
    div.stButton > button p { color: #ffffff !important; font-size: 1.2em !important; }

    /* 結果表示カード */
    .result-card {
        background-color: #ffffff !important; 
        color: #1e1b4b !important;           
        border: 4px solid #818cf8;
        border-radius: 12px;
        padding: 20px;
        margin-top: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. ヘッダー & サイドバー
# ---------------------------------------------------------
st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
try: st.image("GEMINI_gazou.png")
except: st.write("🌌")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<h1 style="text-align: center; color:#e0e7ff;">謝罪DX Ultra</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🏆 ステータス")
    st.metric("累計ポイント", f"{st.session_state.sp_points} SP")
    st.write(f"称号: **{st.session_state.apology_rank}**")

# ---------------------------------------------------------
# 4. 入力エリア (文字は白く設定済み)
# ---------------------------------------------------------
app_mode = st.radio("モード選択：", ["誠心誠意", "他責（Ultra Resilience）"], horizontal=True)

col1, col2 = st.columns(2)
with col1:
    my_name = st.text_input("あなたの名前：", placeholder="例：いしい")
with col2:
    target_name = st.text_input("相手の名前：", placeholder="例：佐藤部長")

user_fact = st.text_area("起きてしまった事象：", placeholder="例：デスクにコーヒーをぶちまけてしまった")

# ボタン配置
if app_mode == "誠心誠意":
    st.markdown('<div class="sincere-btn">', unsafe_allow_html=True)
    execute = st.button("謝罪文案の生成")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="ultra-btn">', unsafe_allow_html=True)
    execute = st.button("言い訳をひねり出す")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. 生成ロジック (429エラー対策込み)
# ---------------------------------------------------------
if execute:
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.error("APIキーが必要です")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            with st.spinner('AIが必死に謝罪/他責中...'):
                response = model.generate_content(f"{user_fact}の謝罪文を150字で。")
                st.session_state.result_text = response.text
                st.session_state.sp_points += random.randint(30, 70)
        except Exception as e:
            if "429" in str(e):
                st.error("【1日の制限に達しました】")
                st.info("APIの無料枠を使い切りました。明日の夕方までお待ちいただくか、新しいAPIキーを設定してください。")
            else:
                st.error(f"エラー: {e}")

if 'result_text' in st.session_state:
    st.markdown(f'<div class="result-card">{st.session_state.result_text}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("©開発者：いしいけいすけ(SME Consultant)")
