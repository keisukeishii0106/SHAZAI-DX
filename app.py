import streamlit as st
import google.generativeai as genai
import random

# ---------------------------------------------------------
# 1. ページ設定 & 状態管理
# ---------------------------------------------------------
st.set_page_config(page_title="謝罪DX Ultra", page_icon="🙇‍♂️", layout="centered")

if 'sp_points' not in st.session_state:
    st.session_state.sp_points = 0
if 'apology_rank' not in st.session_state:
    st.session_state.apology_rank = "見習い謝罪師"

# ---------------------------------------------------------
# 2. デザイン (ボタンの「白」を完全に排除するCSS)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* 全体背景 */
    .stApp { background-color: #1e1b4b; color: #f8fafc; }
    
    /* ロゴのセンタリング */
    .centered-logo { display: flex; justify-content: center; margin-bottom: 30px; }
    .centered-logo img { width: 450px !important; }

    /* タイトルとラベル */
    h1 { text-align: center; color: #e0e7ff; font-weight: 800; }
    div[data-testid="stMarkdownContainer"] p { color: #ffffff !important; font-weight: bold; }
    .stTextInput label, .stTextArea label { color: #ffffff !important; font-weight: bold !important; }

    /* 結果カード */
    .result-card {
        background-color: #ffffff !important; 
        color: #1e1b4b !important;           
        border: 4px solid #818cf8;
        border-radius: 12px;
        padding: 20px;
        font-size: 1.1em;
        margin: 20px 0;
    }

    /* --- ボタンの強制色付け（ここを強化しました） --- */
    
    /* 1. 誠心誠意ボタン (青) */
    .sincere-btn div[data-testid="stButton"] button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .sincere-btn div[data-testid="stButton"] button:hover, 
    .sincere-btn div[data-testid="stButton"] button:active,
    .sincere-btn div[data-testid="stButton"] button:focus {
        background-color: #1d4ed8 !important;
        color: #ffffff !important;
        border: none !important;
    }

    /* 2. 他責ボタン (紫金グラデーション) */
    .ultra-btn div[data-testid="stButton"] button {
        background: linear-gradient(45deg, #7c3aed, #d4af37) !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .ultra-btn div[data-testid="stButton"] button:hover,
    .ultra-btn div[data-testid="stButton"] button:active,
    .ultra-btn div[data-testid="stButton"] button:focus {
        background: linear-gradient(45deg, #6d28d9, #b7952f) !important;
        color: #ffffff !important;
        border: none !important;
    }

    /* ボタン内のテキストが勝手に黒や白に変わるのを防ぐ */
    .stButton p {
        color: #ffffff !important;
        font-weight: 900 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. ヘッダー & サイドバー (変更なし)
# ---------------------------------------------------------
st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
try: st.image("GEMINI_gazou.png")
except: st.write("🌌")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<h1>謝罪DX Ultra</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🏆 謝罪師ステータス")
    st.metric("累計謝罪ポイント (SP)", st.session_state.sp_points)
    st.write(f"現在の称号: **{st.session_state.apology_rank}**")
    st.progress(min(st.session_state.sp_points / 1000, 1.0))

# ---------------------------------------------------------
# 4. メイン入力エリア (プレースホルダ適用済み)
# ---------------------------------------------------------
app_mode = st.radio("モード選択：", ["誠心誠意", "他責（Ultra Resilience）"], horizontal=True)

col1, col2 = st.columns(2)
with col1:
    my_name = st.text_input("あなたの名前：", placeholder="例：いしい")
with col2:
    target_name = st.text_input("相手の名前：", placeholder="例：佐藤部長")

user_fact = st.text_area("起きてしまった事象：", placeholder="例：デスクにコーヒーをぶちまけてしまった")

# モード別のボタン配置
execute = False
if app_mode == "誠心誠意":
    st.markdown('<div class="sincere-btn">', unsafe_allow_html=True)
    execute = st.button("謝罪文案の生成")
    st.markdown('</div>', unsafe_allow_html=True)
    prompt_flavor = "ビジネスとして誠実、再発防止策を含む"
else:
    st.markdown('<div class="ultra-btn">', unsafe_allow_html=True)
    execute = st.button("言い訳をひねり出す")
    st.markdown('</div>', unsafe_allow_html=True)
    prompt_flavor = "自分以外の驚くべき外部要因（宇宙・気象・社会情勢等）へ責任転送"

# ---------------------------------------------------------
# 5. 生成ロジック (変更なし)
# ---------------------------------------------------------
if execute:
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.error("APIキー設定なし")
    elif not user_fact or not target_name:
        st.warning("入力が足りません")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"宛名:{target_name} 差出人:{my_name} 事象:{user_fact}。指令:{prompt_flavor}。200文字程度。"

            with st.spinner('理論構築中...'):
                response = model.generate_content(prompt)
                st.session_state.result_text = response.text
                
                # ポイント加算
                pts = random.randint(30, 70)
                st.session_state.sp_points += pts
                if st.session_state.sp_points > 500: st.session_state.apology_rank = "他責の神"
                elif st.session_state.sp_points > 200: st.session_state.apology_rank = "レジリエンス達人"
                elif st.session_state.sp_points > 50: st.session_state.apology_rank = "中堅謝罪士"
                st.toast(f"成功！ {pts} SP 獲得！")
        except Exception as e:
            st.error(f"エラー: {e}")

if 'result_text' in st.session_state:
    st.markdown(f'<div class="result-card">{st.session_state.result_text}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("©開発者：いしいけいすけ(SME Consultant)")
