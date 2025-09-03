import streamlit as st
import uuid
from utils import get_predictions, insert_sentence, run_sql  # bạn có thể sửa tên tùy theo dự án


def clear_input():
    st.session_state["input_text"] = ""


def analysis_page(conn):
    st.header("📊 Phân tích Cảm Xúc Theo Khía Cạnh Trong Phản Hồi Người Học")

    # Dropdown để chọn model, gọn và căn trái
    col_model, _ = st.columns([2, 8])
    with col_model:
        model_choice = st.selectbox(
            "Chọn model", 
            ["PhoBert_CNN_LSTM", "CNN_LSTM_ATTENTION"],
            help="Chọn PhoBERT hoặc CNN_LSTM_Attention",
            key="model_choice"
        )

    # Nhập câu hoặc tải file
    raw_text = st.text_area("Nhập câu (tiếng Việt):", key="input_text", height=150)
    uploaded = st.file_uploader("… hoặc chọn file .txt", type=["txt"])
    col_clear, col_spacer, col_clf, col_file = st.columns([1, 6, 2.5, 2.5])

    with col_clear:
        st.button(
            "Clear 🧹",
            help="Xoá nội dung",
            use_container_width=True,
            on_click=clear_input
        )

    with col_clf:
        btn_sentence = st.button("Phân tích câu", use_container_width=True)

    with col_file:
        btn_file = st.button("Phân tích file", use_container_width=True)

    # Phân tích từng câu
    if btn_sentence:
        if not raw_text.strip():
            st.warning("Vui lòng nhập văn bản")
        else:
            pairs = get_predictions(raw_text, model=model_choice)
            if pairs:
                st.success("Kết quả:")
                for asp, sen in pairs:
                    st.write(f"• **{asp}** – {sen}")
            else:
                st.info("Không phát hiện cặp (aspect, sentiment) nào.")

    # Phân tích file từng dòng
    if btn_file:
        if uploaded is None:
            st.warning("Chưa chọn file")
        else:
            fname = uploaded.name
            content = uploaded.read().decode("utf-8")
            lines = [l for l in content.splitlines() if l.strip()]
            total = len(lines)

            # Khởi tạo session_state cho stop flag nếu chưa có
            if "stop_file" not in st.session_state:
                st.session_state["stop_file"] = False

            # Hiển thị thanh tiến độ luôn
            progress = st.progress(0)
            # Nút dừng
            if st.button("Stop", key="stop_file_btn"):
                st.session_state["stop_file"] = True

            # Expander luôn mở để giữ container
            exp = st.expander(f"Kết quả phân tích file: {fname}", expanded=True)
            with exp:
                for i, line in enumerate(lines, start=1):
                    # Dừng nếu người dùng nhấn Stop
                    if st.session_state.get("stop_file"):
                        st.warning("Quá trình đã bị dừng bởi người dùng.")
                        break

                    st.write(f"**{line}**")
                    pairs = get_predictions(line, model=model_choice)
                    if pairs:
                        for asp, sen in pairs:
                            st.write(f"  ↳ {asp} – {sen}")
                    else:
                        st.write("  ↳ Không phát hiện.")

                    # Cập nhật tiến độ
                    progress.progress(i / total)
                else:
                    st.success("Hoàn tất phân tích file!")

