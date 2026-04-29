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
# 2. デザイン (視認性重視のパープルスタイル)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* 全体背景と基本文字色 */
    .stApp {
        background-color: #1e1b4b; /* 深い紫 */
        color: #f8fafc;           /* 明るい白 */
    }
    
    /* タイトル周り */
    .header-container { text-align: center; margin-bottom: 20px; }
    h1 { color: #e0e7ff; font-weight: 800; border-bottom: 1px solid #4338ca; }
    
    /* 入力ラベルの視認性向上 */
    label, .stMarkdown { color: #e0e7ff !important; font-weight: 600 !important; }

    /* 生成されたテキストのカード (白背景で絶対的な視認性) */
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

    /* ボタンのカスタマイズ */
    .stButton>button {
        width: 100%; border-radius: 10px; height: 3.5em;
        font-weight: bold; transition: 0.3s;
    }
    /* 誠心誠意：青系 / 他責：紫金系 */
    div[data-testid="stForm"] .stButton>button, .sincere-btn>button {
        background: #3730a3; color: white; border: 1px solid #818cf8;
    }
    .ultra-btn>button {
        background: linear-gradient(45deg, #4c1d95, #d4af37); color: white; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. ヘッダー (ロゴ & タイトル)
# ---------------------------------------------------------
st.markdown('<div class="header-container">', unsafe_allow_html=True)
try:
    # タイトルの上にロゴを大きく配置
    st.image("GEMINI_gazou.png", width=300)
except:
    st.write("🌌")
st.markdown('<h1>謝罪DX Ultra</h1>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. サイドバー (ステータスのみ)
# ---------------------------------------------------------
with st.sidebar:
    st.header("🏆 謝罪師ステータス")
    st.metric("累計謝罪ポイント (SP)", st.session_state.sp_points)
    st.write(f"現在の称号: **{st.session_state.apology_rank}**")
    st.progress(min(st.session_state.sp_points / 1000, 1.0))
    st.caption("※生成を行うたびにポイントが貯まります。")

# ---------------------------------------------------------
# 5. メイン入力エリア
# ---------------------------------------------------------
app_mode = st.radio("モード選択：", ["誠心誠意", "他責（Ultra Resilience）"], horizontal=True)

col1, col2 = st.columns(2)
with col1:
    my_name = st.text_input("あなたの名前：", value="いしい")
with col2:
    target_name = st.text_input("相手の名前：")

user_fact = st.text_area("起きてしまった事象：", placeholder="例：会議の資料を忘れた")

# モード別の設定
if app_mode == "誠心誠意":
    button_label = "謝罪文案の生成"
    btn_class = "sincere-btn"
    prompt_flavor = "ビジネスとして誠実、再発防止策を含む"
else:
    button_label = "言い訳をひねり出す"
    btn_class = "ultra-btn"
    prompt_flavor = "自分以外の驚くべき外部要因（宇宙・気象・社会情勢等）へ責任転送"

# ---------------------------------------------------------
# 6. 生成ロジック (ポイント加算連動)
# ---------------------------------------------------------
st.markdown(f'<div class="{btn_class}">', unsafe_allow_html=True)
if st.button(button_label):
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.error("APIキーが設定されていません。")
    elif not user_fact or not target_name:
        st.warning("名前と事象を入力してください。")
    else:
        try:
            genai.configure(api_key=api_key)
            # モデル検索と選択
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            target_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
            model = genai.GenerativeModel(target_model)

            prompt = f"宛名:{target_name} 差出人:{my_name} 事象:{user_fact}。指令:{prompt_flavor}。200文字程度。"

            with st.spinner('次元を構築中...'):
                response = model.generate_content(prompt)
                st.session_state.result_text = response.text
                
                # --- ミニゲーム連動：成功時にポイント加算 ---
                added_points = random.randint(30, 70)
                st.session_state.sp_points += added_points
                
                # 称号アップデート
                if st.session_state.sp_points > 500: st.session_state.apology_rank = "他責の神"
                elif st.session_state.sp_points > 200: st.session_state.apology_rank = "レジリエンス達人"
                elif st.session_state.sp_points > 50: st.session_state.apology_rank = "中堅謝罪士"
                
                st.toast(f"生成成功！ {added_points} SP 獲得しました！")

        except Exception as e:
            if "429" in str(e):
                st.error("宇宙リソース制限（429エラー）。1分ほどお待ちください。")
            else:
                st.error(f"エラー: {e}")
st.markdown('</div>', unsafe_allow_html=True)

# 結果表示
if 'result_text' in st.session_state:
    st.markdown(f'<div class="result-card">{st.session_state.result_text}</div>', unsafe_allow_html=True)
