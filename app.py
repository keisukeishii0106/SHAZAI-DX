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
# 2. デザイン (最強のボタン上書き設定)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* 全体背景 */
    .stApp { background-color: #1e1b4b; color: #f8fafc; }
    
    /* ロゴのセンタリング */
    .centered-logo { display: flex; justify-content: center; margin-bottom: 30px; }
    .centered-logo img { width: 450px !important; }

    /* 入力ラベルの文字色 */
    label, .stMarkdown p { color: #ffffff !important; font-weight: bold !important; font-size: 1.05em; }

    /* --- ボタンの強制デザイン修正 --- */
    /* ボタンの土台そのものを色付け */
    div.stButton > button {
        border-radius: 12px !important;
        height: 4em !important;
        width: 100% !important;
        border: none !important;
        font-size: 1.2em !important;
        font-weight: 900 !important;
        transition: 0.3s;
    }

    /* 誠心誠意モードの時のボタン（青） */
    .sincere-btn div.stButton > button {
        background-color: #2563eb !important;
        color: #ffffff !important;
    }

    /* 他責モードの時のボタン（紫金グラデーション） */
    .ultra-btn div.stButton > button {
        background: linear-gradient(45deg, #7c3aed, #d4af37) !important;
        color: #ffffff !important;
    }

    /* ボタンの中にある文字を強制的に白くする（これが一番重要でした） */
    div.stButton > button p {
        color: #ffffff !important;
        font-weight: 900 !important;
    }

    /* マウスを乗せた時やクリックした時も白くならないように固定 */
    div.stButton > button:hover, div.stButton > button:active, div.stButton > button:focus {
        color: #ffffff !important;
        opacity: 0.85;
    }

    /* 結果表示カード */
    .result-card {
        background-color: #ffffff !important; 
        color: #1e1b4b !important;           
        border: 4px solid #818cf8;
        border-radius: 12px;
        padding: 20px;
        font-size: 1.1em;
        margin-top: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. ヘッダー & ロゴ
# ---------------------------------------------------------
st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
try: st.image("GEMINI_gazou.png")
except: st.write("🌌 ロゴ画像が見つかりません")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<h1 style="text-align: center;">謝罪DX Ultra</h1>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. サイドバー
# ---------------------------------------------------------
with st.sidebar:
    st.header("🏆 謝罪師ステータス")
    st.metric("累計ポイント", f"{st.session_state.sp_points} SP")
    st.write(f"称号: **{st.session_state.apology_rank}**")
    st.progress(min(st.session_state.sp_points / 1000, 1.0))

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

# --- 実行ボタン（ここにクラスを適用） ---
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
    prompt_flavor = "自分以外の外部要因へ責任転送。宇宙・気象・量子力学等の超理論を展開。"

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
            model = genai.GenerativeModel('gemini-1.5-flash')
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

if 'result_text' in st.session_state:
    st.markdown(f'<div class="result-card">{st.session_state.result_text}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 7. フッター
# ---------------------------------------------------------
st.markdown("---")
st.caption("©開発者：いしいけいすけ(SME Consultant)")
