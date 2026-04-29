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
# 2. デザイン (ボタンを確実に色付け)
# ---------------------------------------------------------
st.markdown("""
    <style>
    .stApp { background-color: #1e1b4b; color: #f8fafc; }
    .centered-logo { display: flex; justify-content: center; margin-bottom: 30px; }
    .centered-logo img { width: 450px !important; }
    label, .stMarkdown p { color: #ffffff !important; font-weight: bold !important; }

    /* ボタンの強制色付け：背景も文字も個別に指定 */
    div.stButton > button {
        width: 100% !important;
        height: 4em !important;
        border-radius: 12px !important;
        border: none !important;
        font-size: 1.2em !important;
        font-weight: 900 !important;
    }

    /* 誠心誠意：青 */
    .sincere-btn div.stButton > button { background-color: #2563eb !important; }
    .sincere-btn div.stButton > button p { color: #ffffff !important; }

    /* 他責：紫金グラデーション */
    .ultra-btn div.stButton > button { background: linear-gradient(45deg, #7c3aed, #d4af37) !important; }
    .ultra-btn div.stButton > button p { color: #ffffff !important; }

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
# 4. メイン入力エリア (プレースホルダ適用済)
# ---------------------------------------------------------
app_mode = st.radio("モード選択：", ["誠心誠意", "他責（Ultra Resilience）"], horizontal=True)

col1, col2 = st.columns(2)
with col1:
    my_name = st.text_input("あなたの名前：", placeholder="例：いしい")
with col2:
    target_name = st.text_input("相手の名前：", placeholder="例：佐藤部長")

user_fact = st.text_area("起きてしまった事こそ：", placeholder="例：デスクにコーヒーをぶちまけてしまった")

# ボタン描画
if app_mode == "誠心誠意":
    st.markdown('<div class="sincere-btn">', unsafe_allow_html=True)
    execute = st.button("謝罪文案の生成")
    st.markdown('</div>', unsafe_allow_html=True)
    prompt_flavor = "ビジネスとして誠実、再発防止策を含む"
else:
    st.markdown('<div class="ultra-btn">', unsafe_allow_html=True)
    execute = st.button("言い訳をひねり出す")
    st.markdown('</div>', unsafe_allow_html=True)
    prompt_flavor = "自分以外の外部要因（宇宙・気象・社会情勢等）へ責任転送"

# ---------------------------------------------------------
# 5. 生成ロジック (モデル名問題を根底から解決)
# ---------------------------------------------------------
if execute:
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.error("APIキーが設定されていません。")
    elif not user_fact or not target_name:
        st.warning("名前と事象を入力してください。")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # 利用可能な全モデルを取得
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # 1.5-flash を優先的に探し、なければリストの先頭を使う
            target_model = ""
            for m in available_models:
                if "gemini-1.5-flash" in m:
                    target_model = m
                    break
            
            if not target_model:
                target_model = available_models[0] # 何でもいいから動くものを掴む

            model = genai.GenerativeModel(target_model)
            prompt = f"宛名:{target_name} 差出人:{my_name} 事象:{user_fact}。指令:{prompt_flavor}。150文字程度。"

            with st.spinner(f'モデル({target_model})で構築中...'):
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
            st.error(f"システムエラー: {e}")

if 'result_text' in st.session_state:
    st.markdown(f'<div class="result-card">{st.session_state.result_text}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("©開発者：いしいけいすけ(SME Consultant)")
