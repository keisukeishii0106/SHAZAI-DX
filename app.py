import streamlit as st
import google.generativeai as genai

# UI設定
st.set_page_config(page_title="不可抗力DX", page_icon="🌌")
st.title("🌌 不可抗力の論理構築アプリ")
st.caption("〜 100%自分の非を、宇宙規模の不可抗力へ昇華させる 〜")

# SecretsからAPIキーを取得
api_key = st.secrets.get("GEMINI_API_KEY", "")

# サイドバー設定
with st.sidebar:
    st.header("Status")
    if api_key:
        st.success("APIキー接続済み：宇宙の法則と同期中")
    else:
        st.error("APIキー未設定：StreamlitのSecretsを確認してください")

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
        st.error("APIキーが設定されていません。")
    elif not user_fact:
        st.warning("言い訳の種となる「事実」を入力してください。")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # 404エラー対策：利用可能なモデルをリストアップして、動くものを自動選択
            model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            if not model_list:
                st.error("利用可能なモデルが見つかりませんでした。")
            else:
                # リストの最初にある有効なモデルを使用
                target_model = model_list[0]
                model = genai.GenerativeModel(target_model)
                
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
                
                with st.spinner(f'超理論（Model: {target_model}）を構築中...'):
                    response = model.generate_content(prompt)
                    st.success("理論構築が完了しました")
                    st.markdown("---")
                    st.markdown(f"### 🚀 構築された超理論")
                    st.write(response.text)
                    st.warning("⚠️ 使用上の注意：信頼関係が崩壊する恐れがあります。")
                    
        except Exception as e:
            st.error(f"エラーが発生しました：{e}")

st.markdown("---")
st.caption("© 2026 不可抗力DX プロジェクトチーム")
