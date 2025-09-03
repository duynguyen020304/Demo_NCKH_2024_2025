import streamlit as st
from analysis_page import analysis_page
from stats_page import stats_page
from setting_page import setting_page
from utils import create_database, create_connection, DB_NAME

def main():
    st.set_page_config(page_title="Aspect-Based Sentiment", layout="wide")
    create_database(DB_NAME)
    conn = create_connection(DB_NAME)

    # Luôn đảm bảo 'page' có trong session
    if "page" not in st.session_state:
        st.session_state.page = "Phân tích"

    # Sidebar navigation
    with st.sidebar:
        st.title("📚 Chức năng")
        if st.button("📊 Phân tích", use_container_width=True):
            st.session_state.page = "Phân tích"
        if st.button("📈 Thống kê", use_container_width=True):
            st.session_state.page = "Thống kê"
        if st.button("⚙️ Cài đặt", use_container_width=True):
            st.session_state.page = "Cài đặt"
        if st.button("❓ Hướng dẫn", use_container_width=True):
            st.session_state.page = "Hướng dẫn"

    # Lấy page hiện tại
    page = st.session_state.get("page", "Phân tích")  # <-- fallback an toàn

    # Hiển thị trang
    if page == "Phân tích":
        analysis_page(conn)
    elif page == "Thống kê":
        stats_page(conn)
    elif page == "Cài đặt":
        setting_page()
    elif page == "Hướng dẫn":
        st.header("❓ Hướng dẫn sử dụng")
        st.markdown("""
        - **Phân tích:** Nhập câu hoặc chọn file `.txt` để trích xuất (aspect, sentiment).
        - **Thống kê:** Xem biểu đồ tổng hợp cảm xúc và khía cạnh.
        - **Cài đặt:** Tuỳ chỉnh cấu hình giao diện.
        """)
    else:
        st.warning("Không xác định được trang, vui lòng chọn lại từ sidebar.")

if __name__ == "__main__":
    main()
