# setting_page.py
import streamlit as st

# ========= Cấu hình mặc định =========
DEFAULT_CHART_COLORS = {
    "positive": "#2ECC71",   # xanh lá
    "negative": "#E74C3C",   # đỏ
    "neutral":  "#F1C40F",   # vàng
}

def setting_page():
    st.header("⚙️ Cài đặt")

    # -----------------------------------------------------------
    # 1) Tùy chọn màu cho biểu đồ (sử dụng ở stats_page)
    # -----------------------------------------------------------
    st.subheader("🎨 Tuỳ chỉnh màu biểu đồ cảm xúc")

    # Khởi tạo session_state.chart_colors nếu chưa có
    if "chart_colors" not in st.session_state:
        st.session_state.chart_colors = DEFAULT_CHART_COLORS.copy()

    # Hiển thị color‑picker cho từng nhãn
    changed = False
    for label, default_color in st.session_state.chart_colors.items():
        new_color = st.color_picker(f"Màu cho **{label}**", value=default_color, key=f"color_{label}")
        if new_color != st.session_state.chart_colors[label]:
            st.session_state.chart_colors[label] = new_color
            changed = True

    if changed:
        st.success("✅ Đã lưu màu mới. Mở lại trang **Thống kê** để xem thay đổi!")

    # -----------------------------------------------------------
    # 2) (Tuỳ chọn) Đổi font toàn app – tiêm CSS động
    # -----------------------------------------------------------
    st.subheader("🖋️ Tuỳ chỉnh font chữ (toàn ứng dụng)")

    # Danh sách một số font web an toàn
    fonts = ["Roboto", "Inter", "Helvetica", "Arial", "Times New Roman", "Georgia", "Courier New"]
    if "app_font" not in st.session_state:
        st.session_state.app_font = fonts[0]

    font_sel = st.selectbox("Chọn font hiển thị", fonts, index=fonts.index(st.session_state.app_font))
    if font_sel != st.session_state.app_font:
        st.session_state.app_font = font_sel
        st.rerun()   # reload để CSS áp dụng ngay

    # Inject CSS (chạy mỗi lần rerun)
    st.markdown(
        f"""
        <style>
            html, body, [class*="css"] {{
                font-family: '{st.session_state.app_font}', sans-serif !important;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------------
    st.divider()
    st.info("Các tuỳ chọn khác sẽ được bổ sung trong phiên bản sắp tới.")
