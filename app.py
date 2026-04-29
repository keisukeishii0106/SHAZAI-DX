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
    .stApp { background-color: #1e1b4b; color: #f8fafc; }
    .centered-logo { display: flex; justify-content: center; margin-bottom: 20px; }
    .centered-logo img { width: 450px !important; }

    /* モード選択の文字を白く太く */
    div[data-testid="stRadio"] label p {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 1.15em !important;
    }
    
    .stTextInput label, .stTextArea label { color: #ffffff !important; font-weight: bold !important; }

    /* --- 生成ボタンのデザイン --- */
    div.stButton > button {
        width: 100% !important;
        height: 4.5em !important;
        border-radius: 15px !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        font-weight: 900 !important;
        transition: all 0.3s ease;
    }

    /* 誠心誠意モード：ビジネスブルー */
    .sincere-btn div.stButton > button {
        background: linear-gradient(135deg, #2563eb, #1e40af) !important;
        color: #ffffff !important;
    }

    /* 他責モード：宇宙グラデーション */
    .ultra-btn div.stButton > button {
        background: linear-gradient(135deg, #4c1d95, #7c3aed, #d4af37) !important;
        background-size: 200% 200% !important;
        color: #ffffff !important;
        animation: space-shimmer 3s ease infinite;
        border: 2px solid #d4af37 !important;
    }

    @keyframes space-shimmer {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    div.stButton > button p { color: #ffffff !important; font-size: 1.3em !important; }

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
with col1: my_name = st.text_input("あなたの名前：", placeholder="例：いしい")
with col2: target_name = st.text_input("相手の名前：", placeholder="例：佐藤部長")
user_fact = st.text_area("起きてしまった事象：", placeholder="例：デスクにコーヒーをぶちまけてしまった")

if app_mode == "誠心誠意":
    st.markdown('<div class="sincere-btn">', unsafe_allow_html=True)
    execute = st.button("誠意を込めて生成")
    st.markdown('</div>', unsafe_allow_html=True)
    prompt_flavor = "ビジネスとして誠実、再発防止策を含む"
else:
    st.markdown('<div class="ultra-btn">', unsafe_allow_html=True)
    execute = st.button("宇宙の理で言い訳する")
    st.markdown('</div>', unsafe_allow_html=True)
    prompt_flavor = "自分以外の外部要因へ責任転送。宇宙・気象・量子力学等の超理論を展開。"

# ---------------------------------------------------------
# 5. 生成ロジック（404エラー対策：自動モデル選別）
# ---------------------------------------------------------
if execute:
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.error("APIキーが必要です")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # 【404対策】使えるモデルを動的に取得
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # gemini-1.5-flashがあれば使い、なければ最初に見つかったモデルを使う
            model_name = "models/gemini-1.5-flash"
            if model_name not in models:
                model_name = models[0] if models else None
            
            if not model_name:
                st.error("利用可能なAIモデルが見つかりません。")
            else:
                model = genai.GenerativeModel(model_name)
                with st.spinner(f'AI({model_name})が構築中...'):
                    response = model.generate_content(f"{user_fact}の謝罪文を150文字程度。指令：{prompt_flavor}")
                    st.session_state.result_text = response.text
                    
                    # 成功時にポイント加算
                    pts = random.randint(30, 70)
                    st.session_state.sp_points += pts
                    if st.session_state.sp_points > 500: st.session_state.apology_rank = "他責の神"
                    elif st.session_state.sp_points > 200: st.session_state.apology_rank = "レジリエンス達人"
                    elif st.session_state.sp_points > 50: st.session_state.apology_rank = "中堅謝罪士"
                    st.toast(f"成功！ {pts} SP 獲得！")
                    
        except Exception as e:
            if "429" in str(e):
                st.error("【API制限中】1日の上限に達しました。明日復活します！")
            else:
                st.error(f"システムエラー: {e}")

if 'result_text' in st.session_state:
    st.markdown(f'<div class="result-card">{st.session_state.result_text}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("©開発者：いしいけいすけ(SME Consultant)")
