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
# 2. デザイン (宇宙ボタン & モード文字白化)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* 全体背景 */
    .stApp { background-color: #1e1b4b; color: #f8fafc; }
    
    /* ロゴのセンタリング */
    .centered-logo { display: flex; justify-content: center; margin-bottom: 20px; }
    .centered-logo img { width: 450px !important; }

    /* モード選択の文字を「絶対」白く太く */
    div[data-testid="stRadio"] label p {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 1.15em !important;
    }
    
    /* 入力欄ラベルの白化 */
    .stTextInput label, .stTextArea label {
        color: #ffffff !important;
        font-weight: bold !important;
    }

    /* --- 生成ボタンのデザイン --- */
    div.stButton > button {
        width: 100% !important;
        height: 4.5em !important;
        border-radius: 15px !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        font-weight: 900 !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }

    /* 誠心誠意モード：清潔感のあるビジネスブルー */
    .sincere-btn div.stButton > button {
        background: linear-gradient(135deg, #2563eb, #1e40af) !important;
        color: #ffffff !important;
    }

    /* 他責モード：【復活】宇宙グラデーション */
    .ultra-btn div.stButton > button {
        background: linear-gradient(135deg, #4c1d95, #7c3aed, #d4af37) !important;
        background-size: 200% 200% !important;
        color: #ffffff !important;
        animation: space-shimmer 3s ease infinite;
        border: 2px solid #d4af37 !important; /* 金の縁取り */
    }

    @keyframes space-shimmer {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ボタンの中の文字 */
    div.stButton > button p {
        color: #ffffff !important;
        font-size: 1.3em !important;
        letter-spacing: 2px;
    }

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
# 3. ヘッダー
# ---------------------------------------------------------
st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
try: st.image("GEMINI_gazou.png")
except: st.write("🌌")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<h1 style="text-align: center; color:#e0e7ff;">謝罪DX Ultra</h1>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. 入力エリア
# ---------------------------------------------------------
app_mode = st.radio("モード選択：", ["誠心誠意", "他責（Ultra Resilience）"], horizontal=True)

col1, col2 = st.columns(2)
with col1:
    my_name = st.text_input("あなたの名前：", placeholder="例：いしい")
with col2:
    target_name = st.text_input("相手の名前：", placeholder="例：佐藤部長")

user_fact = st.text_area("起きてしまった事象：", placeholder="例：デスクにコーヒーをぶちまけてしまった")

# --- 宇宙ボタンの配置 ---
if app_mode == "誠心誠意":
    st.markdown('<div class="sincere-btn">', unsafe_allow_html=True)
    execute = st.button("誠意を込めて生成")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="ultra-btn">', unsafe_allow_html=True)
    execute = st.button("宇宙の理で言い訳する")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. ロジック
# ---------------------------------------------------------
if execute:
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.error("APIキー未設定です")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            with st.spinner('計算中...'):
                response = model.generate_content(f"{user_fact}の謝罪文を。")
                st.session_state.result_text = response.text
        except Exception as e:
            if "429" in str(e):
                st.error("【API制限中】1日の上限を超えました。")
                st.info("見た目の確認は完了です！明日の復活をお楽しみに！")
            else:
                st.error(f"エラー: {e}")

if 'result_text' in st.session_state:
    st.markdown(f'<div class="result-card">{st.session_state.result_text}</div>', unsafe_allow_html=True)

st.caption("©開発者：いしいけいすけ(SME Consultant)")
