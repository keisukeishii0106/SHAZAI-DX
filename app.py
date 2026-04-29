import streamlit as st

# ページの設定（タブに表示される名前など）
st.set_page_config(page_title="Professional Dashboard", layout="centered")

# --- デザインと色味の反映 (CSS) ---
st.markdown("""
    <style>
        /* お気に入りの配色を定義 */
        :root {
            --primary-color: #2c3e50;
            --accent-color: #e74c3c;
            --bg-light: #f4f7f6;
        }

        /* メイン背景とフォントの設定 */
        .stApp {
            background-color: #f4f7f6;
        }

        /* ヘッダーエリア */
        .custom-header {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 0 0 15px 15px;
            border-bottom: 4px solid #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }

        .brand-text {
            font-size: 1.8rem;
            font-weight: 800;
            color: #2c3e50;
            letter-spacing: 2px;
        }

        /* ヒーローエリア */
        .hero-section {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 40px 20px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 30px;
        }

        /* カードデザイン */
        .info-card {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
            border-left: 5px solid #e74c3c;
        }
    </style>
    """, unsafe_allow_html=True)

# --- 画面構成の作成 ---

# 1. カスタムヘッダー
st.markdown('<div class="custom-header"><span class="brand-text">SYSTEM DASHBOARD</span></div>', unsafe_allow_html=True)

# 2. ヒーローセクション
st.markdown("""
    <div class="hero-section">
        <h1>Strategic Overview</h1>
        <p>こだわりの色味とモダンなレイアウトを維持した軽量版です。</p>
    </div>
    """, unsafe_allow_html=True)

# 3. メインコンテンツ（カード）
st.markdown("""
    <div class="info-card">
        <h2 style="color: #2c3e50; margin-top: 0;">Design Logic</h2>
        <p>ロゴ画像の代わりに、CSSによるスタイリングで洗練された印象を作っています。<br>
        Streamlitの標準コンポーネントとカスタムHTMLを組み合わせた構成です。</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Streamlit標準のボタンも色味を合わせる（参考）
if st.button("詳細データを確認する"):
    st.balloons()
    st.success("ボタンが押されました。ここに機能を実装できます！")

# 5. フッター
st.markdown("""
    <div style="text-align: center; margin-top: 50px; color: #95a5a6; font-size: 0.8rem;">
        &copy; 2026 Management Strategy Office.
    </div>
    """, unsafe_allow_html=True)
