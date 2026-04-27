import streamlit as st
import google.generativeai as genai

# UI設定
st.set_page_config(page_title="不可抗力DX", page_icon="🌌")
st.title("🌌 不可抗力の論理構築アプリ")
st.caption("〜 100%自分の非を、宇宙規模の不可抗力へ昇華させる 〜")

# サイドバーでAPIキー設定
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("APIキーを入力して、超理論を起動してください。")

# 入力セクション
st.subheader("1. 事実の入力")
user_fact = st.text_area("「自分が悪い」事実を正直に書いてください", 
                         placeholder="例：昨日飲みすぎて、今起きた（現在11:00）")

st.subheader("2. 言い訳モードの選択")
mode = st.radio(
    "相手を黙らせる論理を選択してください：",
    ["【鉄壁の論理】（専門用語で脳をフリーズさせる）", 
     "【涙の情緒】（怒る方が悪い雰囲気に持ち込む）", 
     "【責任転送】（量子力学や太陽フレアのせいにする）"]
)

# 生成ボタン
if st.button("超理論へ変換する"):
    if not api_key:
        st.error("APIキーが入力されていません。サイドバーから入力してください。")
    elif not user_fact:
        st.warning("言い訳の種となる「事実」を入力してください。")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # モードに合わせたプロンプト調整
        prompt = f"""
        あなたは「世界最高の言い訳コンサルタント」です。
        以下の「100%自分が悪い事実」を、指定されたモードで「個人の意志ではどうしようもなかった不可抗力」へと変換してください。
        
        【事実】: {user_fact}
        【選択モード】: {mode}
        
        【変換ルール】:
        1. 自分の非を一切認めないこと。
        2. {mode}の特性を最大限に活かし、相手が反論する気をなくす文章にすること。
        3. 結論として「これはむしろ歓迎すべき事態である」または「私は被害者である」というスタンスを貫くこと。
        """
        
        with st.spinner('超理論を構築中...'):
            try:
                response = model.generate_content(prompt)
                st.success("理論構築が完了しました")
                st.markdown("---")
                st.markdown(f"### 🚀 構築された超理論")
                st.write(response.text)
                st.warning("⚠️ 使用上の注意：信頼関係が崩壊する恐れがあります。")
            except Exception as e:
                st.error(f"エラーが発生しました：{e}")

# フッター
st.markdown("---")
st.caption("© 2026 不可抗力DX プロジェクトチーム")
