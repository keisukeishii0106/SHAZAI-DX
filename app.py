st.subheader("🎲 運命のスパイス（隠し味）")
gacha_list = [
    "なし", "太陽フレアの影響", "水星の逆行", "量子力学的なゆらぎ", 
    "徳の積みが足りなかった", "並行世界の自分との同期", "バタフライエフェクト"
]
spice = st.selectbox("言い訳に混ぜる「不可抗力」を選んでください：", gacha_list)

mode = st.select_slider(
    "理論の強度（他責レベル）：",
    options=["平謝り（初心者）", "論理的防壁（プロ）", "次元の彼方（神）"]
)

# 生成ボタン
if st.button("超理論を次元構築する"):
    if not api_key:
        st.error("APIキーが未設定です")
    elif not user_fact or not target_name:
        st.warning("名前と罪状を入力してください")
    else:
        try:
            genai.configure(api_key=api_key)
            model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            target_model = model_list[0] if model_list else 'gemini-1.5-flash'
            model = genai.GenerativeModel(target_model)
            
            # プロンプトの構築（スパイス注入）
            prompt = f"""
            あなたは世界最高の言い訳コンサルタントです。
            【宛名】: {target_name}
            【差出人】: {my_name}
            【事実】: {user_fact}
            【隠し味】: {spice}
            【モード】: {mode}
            
            【指令】:
            1. 冒頭は「{target_name}様、お世話になっております。{my_name}です。」で開始。
            2. 200文字以内で作成。
            3. {spice}を原因として論理的に組み込み、個人の努力では回避不能だったことを証明せよ。
            4. 結論として「これはむしろ次世代の働き方である」的なポジティブな着地をせよ。
            """
            
            with st.spinner('宇宙の意志を確認中...'):
                response = model.generate_content(prompt)
                st.session_state.result = response.text
                
                # おふざけ機能②：クビ覚悟メーター（ランダム風AI診断）
                st.session_state.risk = random.randint(0, 100)
                st.success("理論構築完了！")
        except Exception as e:
            st.error(f"Error: {e}")

# ---------------------------------------------------------
# 3. 表示 & 送信
# ---------------------------------------------------------
if 'result' in st.session_state:
    st.markdown("---")
    st.markdown(f"### 📄 構築された超理論")
    st.info(st.session_state.result)
    
    # リスク分析表示
    risk = st.session_state.risk
    st.write(f"📊 **リスク分析：クビになる確率 {risk}%**")
    if risk < 30:
        st.success("判定：セーフ。相手は困惑していますが、許されます。")
    elif risk < 70:
        st.warning("判定：イエローカード。始末書の準備をしてください。")
    else:
        st.error("判定：ジ・エンド。Net Dreamersの席がなくなっている可能性があります。")

    st.subheader("📩 責任転送（Gmail送信）")
    dest_email = st.text_input("送信先メールアドレス：", placeholder="boss@example.com")
    
    if st.button("この理論を送信する（勇気を持って）"):
        try:
            # カッコいい署名を追加
            final_text = f"{st.session_state.result}\n\n---\n{my_name}\nSME Consultant | DX Strategist\nSent from Shazai DX Ultra"
            
            msg = MIMEText(final_text)
            msg['Subject'] = f"【極秘】本日の事象に関する戦略的報告（{my_name}）"
            msg['From'] = gmail_user
            msg['To'] = dest_email
            msg['Date'] = formatdate(localtime=True)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(gmail_user, gmail_password)
                smtp.send_message(msg)
            
            st.balloons()
            st.success(f"ミッション完了。{dest_email} はもうあなたの術中です。")
        except Exception as e:
            st.error(f"送信エラー: {e}")

st.markdown("---")
st.caption(f"監修: {my_name} (Registered SME Consultant)")
