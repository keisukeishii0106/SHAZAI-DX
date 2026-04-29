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
# 2. デザイン (視認性・ボタン色の徹底修正)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* 全体背景：深い紫 */
    .stApp {
        background-color: #1e1b4b; 
        color: #f8fafc;
    }
    
    /* ロゴのセンタリングと拡大 */
    .centered-logo {
        display: flex;
        justify-content: center;
        margin-bottom: 30px;
    }
    .centered-logo img {
        width: 450px !important; /* さらに大きく設定 */
    }

    /* タイトル */
    h1 { text-align: center; color: #e0e7ff; font-weight: 800; }
    
    /* ラジオボタン（モード選択）の文字色を白く強調 */
    div[data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
        font-size: 1.1em;
        font-weight: bold;
    }

    /* 入力欄のラベル（あなたの名前等）の視認性 */
    .stTextInput label, .stTextArea label {
        color: #ffffff !important;
        font-weight: bold !important;
    }

    /* 生成されたテキストのカード (視認性抜群の白背景) */
    .result-card {
        background-color: #ffffff !important; 
        color: #1e1b4b !important;           
        border: 4px solid #818cf8;
        border-radius: 12px;
        padding: 20px;
        font-size: 1.1em;
        line-height: 1.6;
        margin: 20px 0;
    }

    /* ボタンの共通スタイル */
    .stButton>button {
        width: 100%; border-radius: 10px; height: 3.5em;
        font-weight: 900 !important; font-size: 1.1em !important;
        transition: 0.3s;
        border: none;
        display: block !important;
    }

    /* 誠心誠意ボタン：ハッキリとした青 */
    .sincere-btn .stButton>button {
        background-color: #2563eb !important; 
        color: #ffffff !important;
    }
    .sincere-btn .stButton>button:hover {
        background-color: #1d4ed8 !important;
    }

    /* 他責ボタン：ハッキリとした紫金 */
    .ultra-btn .stButton>button {
        background: linear-gradient(45deg, #7c3aed, #d4af37) !important;
        color: #ffffff !important;
    }
    .ultra-btn .stButton>button:hover {
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. ヘッダー (ロゴ・センタリング & タイトル)
# ---------------------------------------------------------
st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
try:
    st.image("GEMINI_gazou.png") # CSSでサイズと位置を制御
except:
    st.write("🌌")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<h1>謝罪DX Ultra</h1>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. サイドバー
# ---------------------------------------------------------
with st.sidebar:
    st.header("🏆 謝罪師ステータス")
    st.metric("累計謝罪ポイント (SP)", st.session_state.sp_points)
    st.write(f"現在の称号: **{st.session_state.apology_rank}**")
    st.progress(min(st.session_state.sp_points / 1000, 1.0))
    st.caption("※謝罪文の生成に成功するとポイント獲得。")

# ---------------------------------------------------------
# 5. メイン入力エリア (プレースホルダ修正)
# ---------------------------------------------------------
app_mode = st.radio("モード選択：", ["誠心誠意", "他責（Ultra Resilience）"], horizontal=True)

col1, col2 = st.columns(2)
with col1:
    my_name = st.text_input("あなたの名前：", placeholder="例：いしい")
with col2:
    target_name = st.text_input("相手の名前：", placeholder="例：佐藤部長")

user_fact = st.text_area("起きてしまった事象：", placeholder="例：デスクにコーヒーをぶちまけてしまった")

# モード別の設定
if app_mode == "誠心誠意":
    button_label = "謝罪文案の生成"
    btn_container = st.container()
    with btn_container:
        st.markdown('<div class="sincere-btn">', unsafe_allow_html=True)
        execute = st.button(button_label)
        st.markdown('</div>', unsafe_allow_html=True)
    prompt_flavor = "ビジネスとして誠実、再発防止策を含む"
else:
    button_label = "言い訳をひねり出す"
    btn_container = st.container()
    with btn_container:
        st.markdown('<div class="ultra-btn">', unsafe_allow_html=True)
        execute = st.button(button_label)
        st.markdown('</div>', unsafe_allow_html=True)
    prompt_flavor = "自分以外の驚くべき外部要因（宇宙・気象・社会情勢等）へ責任転送"

# ---------------------------------------------------------
# 6. 生成ロジック
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
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            target_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
            model = genai.GenerativeModel(target_model)

            prompt = f"宛名:{target_name} 差出人:{my_name} 事象:{user_fact}。指令:{prompt_flavor}。200文字程度。"

            with st.spinner('理論構築中...'):
                response = model.generate_content(prompt)
                st.session_state.result_text = response.text
                
                # ポイント加算
                added_points = random.randint(30, 70)
                st.session_state.sp_points += added_points
                if st.session_state.sp_points > 500: st.session_state.apology_rank = "他責の神"
                elif st.session_state.sp_points > 200: st.session_state.apology_rank = "レジリエンス達人"
                elif st.session_state.sp_points > 50: st.session_state.apology_rank = "中堅謝罪士"
                st.toast(f"生成成功！ {added_points} SP 獲得！")

        except Exception as e:
            if "429" in str(e):
                st.error("API制限中です。1分ほど待ってから再試行してください。")
            else:
                st.error(f"エラー: {e}")

# 結果表示
if 'result_text' in st.session_state:
    st.markdown(f'<div class="result-card">{st.session_state.result_text}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 7. キャプション (フッター)
# ---------------------------------------------------------
st.markdown("---")
st.caption("©開発者：いしいけいすけ(SME Consultant)")
