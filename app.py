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
# 2. デザイン (最強のボタン上書き)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* 全体背景 */
    .stApp { background-color: #1e1b4b; color: #f8fafc; }
    
    /* ロゴのセンタリング */
    .centered-logo { display: flex; justify-content: center; margin-bottom: 30px; }
    .centered-logo img { width: 450px !important; }

    /* 入力ラベル */
    label, .stMarkdown p { color: #ffffff !important; font-weight: bold !important; }

    /* --- ボタンの強制色付け：クラスをより具体的に --- */
    /* 全ボタン共通 */
    div.stButton > button {
        width: 100% !important;
        height: 4em !important;
        border-radius: 12px !important;
        border: none !important;
        font-size: 1.2em !important;
        font-weight: 900 !important;
    }

    /* 誠心誠意（青）: 疑似クラスまで全て塗りつぶす */
    .sincere-btn div.stButton > button {
        background-color: #2563eb !important;
        color: #ffffff !important;
    }
    .sincere-btn div.stButton > button p { color: #ffffff !important; }

    /* 他責（紫金グラデーション） */
    .ultra-btn div.stButton > button {
        background: linear-gradient(45deg, #7c3aed, #d4af37) !important;
        color: #ffffff !important;
    }
    .ultra-btn div.stButton > button p { color: #ffffff !important; }

    /* 結果表示カード */
    .result-card {
        background-color: #ffffff !important; 
        color: #1e1b4b !important;           
        border: 4px solid #818cf8;
        border-radius: 12px;
        padding: 20px;
        margin-top: 25px;
        font-weight: 500;
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
# 4. サイドバー
# ---------------------------------------------------------
with st.sidebar:
    st.header("🏆 ステータス")
    st.metric("累計ポイント", f"{st.session_state.sp_points} SP")
    st.write(f"称号: **{st.session_state.apology_rank}**")

# ---------------------------------------------------------
# 5. メイン入力エリア
# ---------------------------------------------------------
app_mode = st.radio("モード選択：", ["誠心誠意", "他責（Ultra Resilience）"], horizontal=True)

col1, col2 = st.columns(2)
with col1:
    my_name = st.text_input("あなたの名前：", placeholder="例：いしい")
with col2:
    target_name = st.text_input("相手の名前：", placeholder="例：佐藤部長")

user_fact = st.text_area("起きてしまった事象：", placeholder="例：デスクにコーヒーをぶちまけてしまった")

# --- 実行ボタン（確実にクラスを当てる構造） ---
if app_mode == "誠心誠意":
    st.markdown('<div class="sincere-btn">', unsafe_allow_html=True)
    execute = st.button("謝罪文案の生成")
    st.markdown('</div>', unsafe_allow_html=True)
    prompt_flavor = "ビジネスとして誠実、再発防止策を含む"
else:
    st.markdown('<div class="ultra-btn">', unsafe_allow_html=True)
    execute = st.button("言い訳をひねり出す")
    st.markdown('</div>', unsafe_allow_html=True)
    prompt_flavor = "自分以外の外部要因へ責任転送。宇宙・気象・量子力学等の超理論を展開。"

# ---------------------------------------------------------
# 6. 生成ロジック (404エラー対策・動的モデル取得)
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
            
            # 【重要】利用可能なモデルを動的に取得して404を回避
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # 優先的にflashモデルを探す（models/プレフィックス付き）
            model_name = "models/gemini-1.5-flash" 
            if model_name not in available_models:
                # もし1.5-flashがなければ、リストの最初にある有効なモデルを使う
                model_name = available_models[0] if available_models else "models/gemini-pro"

            model = genai.GenerativeModel(model_name)
            prompt = f"宛名:{target_name} 差出人:{my_name} 事象:{user_fact}。指令:{prompt_flavor}。150文字程度。"

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
            st.error(f"エラーが発生しました: {e}")
            st.info("APIキーの有効性や、モデルの利用権限を確認してください。")

if 'result_text' in st.session_state:
    st.markdown(f'<div class="result-card">{st.session_state.result_text}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("©開発者：いしいけいすけ(SME Consultant)")
