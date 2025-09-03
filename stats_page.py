import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from matplotlib.colors import to_hex
import numpy as np

from utils import get_lists, create_connection

# ==== Hàm lấy palette động đủ dài ====
def get_palette_hex(n, palette_name="Set2"):
    """Trả về danh sách mã HEX màu, dài ít nhất n màu.
    Nếu palette mặc định không đủ, sinh thêm bằng cách lặp lại và xáo trộn."""
    base = sns.color_palette(palette_name)
    if n <= len(base):
        pal = base[:n]
    else:
        repeats = (n // len(base)) + 1
        pal = (base * repeats)[:n]
        np.random.seed(42)
        idx = np.random.permutation(n)
        pal = [pal[i] for i in idx]
    return [to_hex(c) for c in pal]

def get_bright_palette_hex(n):
    return get_palette_hex(n, palette_name="bright")

def stats_page(conn):
    # --- Style chung ---
    sns.set_style("whitegrid")
    plt.rcParams['font.family'] = 'DejaVu Sans'

    # --- Load dữ liệu ---
    sql = """
    SELECT S.text,
           A.name    AS aspect,
           Sen.name  AS sentiment,
           Sem.name  AS semester,
           Cou.code||' – '||Cou.name AS course,
           Cl.name   AS class
    FROM Sentence S
      LEFT JOIN Aspect    A   ON S.aspect_id    = A.id
      LEFT JOIN Sentiment Sen ON S.sentiment_id = Sen.id
      LEFT JOIN Semester  Sem ON S.semester_id  = Sem.id
      LEFT JOIN Course    Cou ON S.course_id    = Cou.id
      LEFT JOIN Class     Cl  ON S.class_id     = Cl.id
    """
    df_full = pd.read_sql_query(sql, conn)

    # --- Sidebar chung ---
    st.sidebar.header("Bộ lọc chung")
    aspects_all    = get_lists(conn, "Aspect")
    sentiments_all = get_lists(conn, "Sentiment")
    semesters_all  = get_lists(conn, "Semester")[:8]
    classes_all    = get_lists(conn, "Class")[:8]
    courses_raw    = conn.execute("SELECT code, name FROM Course").fetchall()
    courses_all    = [f"{c[0]} – {c[1]}" for c in courses_raw]

    sel_aspects   = st.sidebar.multiselect("Khía cạnh", aspects_all,    default=aspects_all)
    sel_sents     = st.sidebar.multiselect("Cảm xúc",   sentiments_all, default=sentiments_all)
    sel_semesters = st.sidebar.multiselect("Học kỳ",    semesters_all,  default=semesters_all)
    sel_courses   = st.sidebar.multiselect("Môn học",   courses_all,    default=courses_all)
    sel_classes   = st.sidebar.multiselect("Lớp",       classes_all,    default=classes_all)

    # palette cho tags (không đổi)
    PALETTE_HEX      = get_palette_hex(max(len(aspects_all), len(sentiments_all)))
    BRIGHT_HEX       = get_bright_palette_hex(len(courses_all))
    CLASS_TAG_COLOR  = "#e0e0e0"

    # CSS cho multiselect tags
    css = "<style>"
    css += ".stSidebar .stMultiSelect div[data-baseweb='select'] span[data-baseweb='tag'] { color: black !important; }"
    num_aspects = len(aspects_all)
    num_sents   = len(sentiments_all)
    for idx, color in enumerate(PALETTE_HEX, start=1):
        if idx <= num_aspects:
            css += (f".stSidebar .stMultiSelect:nth-of-type(1) div[data-baseweb='select'] "
                    f"span[data-baseweb='tag']:nth-child({idx}){{background-color:{color};}}")
        if idx <= num_sents:
            css += (f".stSidebar .stMultiSelect:nth-of-type(2) div[data-baseweb='select'] "
                    f"span[data-baseweb='tag']:nth-child({idx}){{background-color:{color};}}")
    for idx, color in enumerate(BRIGHT_HEX, start=1):
        css += (f".stSidebar .stMultiSelect:nth-of-type(4) div[data-baseweb='select'] "
                f"span[data-baseweb='tag']:nth-child({idx}){{background-color:{color};}}")
    css += (".stSidebar .stMultiSelect:nth-of-type(5) div[data-baseweb='select'] "
            "span[data-baseweb='tag']{background-color:%s;}" % CLASS_TAG_COLOR)
    css += "</style>"
    st.markdown(css, unsafe_allow_html=True)

    # --- Áp dụng bộ lọc chung ---
    df1 = df_full[
        df_full['aspect'].isin(sel_aspects) &
        df_full['sentiment'].isin(sel_sents) &
        df_full['semester'].isin(sel_semesters) &
        df_full['course'].isin(sel_courses) &
        df_full['class'].isin(sel_classes)
    ]

    st.header("📈 Thống kê chi tiết")
    st.markdown("Phân tích dữ liệu câu phản hồi theo nhiều chiều.")
    st.write(f"### Tổng cộng {len(df1)} câu sau khi áp dụng bộ lọc chung")
    if df1.empty:
        st.warning("Không có dữ liệu sau khi áp dụng lọc chung.")
        return
    if st.checkbox("Hiển thị dữ liệu gốc (lọc chung)"):
        st.dataframe(df1)

    # --- Section 1: Pie & Bar cơ bản (giữ nguyên) ---
    st.markdown("---")
    sen_counts = df1['sentiment'].value_counts()
    asp_counts = df1['aspect'].value_counts()
    sen_palette = get_palette_hex(len(sen_counts))
    asp_palette = get_palette_hex(len(asp_counts))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    ax1.pie(sen_counts, labels=sen_counts.index, autopct='%1.1f%%',
            startangle=90, colors=sen_palette, pctdistance=0.75)
    ax1.set_title("Tỷ lệ Cảm xúc"); ax1.axis('equal')

    ax2.pie(asp_counts, labels=None, autopct='%1.1f%%',
            startangle=60, colors=asp_palette, pctdistance=0.75)
    ax2.set_title("Tỷ lệ Khía cạnh"); ax2.axis('equal')
    ax2.legend(asp_counts.index, title="Khía cạnh",
               loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8)
    fig.tight_layout(); st.pyplot(fig)

    st.markdown("---")
    st.subheader("📊 Phân bổ Cảm xúc & Khía cạnh")
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(6, 4))
        sen_counts.plot.bar(color=sen_palette, ax=ax, rot=0)
        ax.set_xlabel("Cảm xúc"); ax.set_ylabel("Số câu")
        fig.tight_layout(); st.pyplot(fig)
    with col2:
        labels = asp_counts.index.tolist()
        vals   = asp_counts.values.tolist() + asp_counts.values[:1].tolist()
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist() + [0]
        fig2, ax2 = plt.subplots(figsize=(6, 4), subplot_kw=dict(polar=True))
        color = asp_palette[0] if asp_palette else "#348ABD"
        ax2.plot(angles, vals, color=color)
        ax2.fill(angles, vals, color=color, alpha=0.25)
        ax2.set_xticks(angles[:-1]); ax2.set_xticklabels(labels, fontsize=8)
        ax2.set_title("Khía cạnh", y=1.1); st.pyplot(fig2)

    # --- ĐỊNH NGHĨA MÀU CỐ ĐỊNH CHO SENTIMENT ---
    sentiment_colors = {
        'Positive': '#66c2a5',
        'Negative': '#fc8d62',
        'Neutral':  '#8da0cb'
    }

    # --- Section 3: Cross-analysis với màu cố định ---
    st.markdown("---")
    st.subheader("🔄 So sánh chéo")
    with st.expander("Bộ lọc cho so sánh chéo"):
        ca_sem = st.selectbox("Học kỳ (cross)", ["Tất cả"] + semesters_all, key="ca_sem")
        ca_cou = st.selectbox("Môn (cross)",   ["Tất cả"] + courses_all,   key="ca_cou")
        ca_cla = st.selectbox("Lớp (cross)",   ["Tất cả"] + classes_all,   key="ca_cla")

    df2 = df_full.copy()
    if ca_sem != "Tất cả": df2 = df2[df2['semester'] == ca_sem]
    if ca_cou != "Tất cả": df2 = df2[df2['course']   == ca_cou]
    if ca_cla != "Tất cả": df2 = df2[df2['class']    == ca_cla]

    dim  = st.selectbox("Chọn chiều X",
                        ['aspect', 'semester', 'course', 'class'], index=0)
    grp  = df2.groupby([dim, 'sentiment']).size().unstack(fill_value=0)

    if grp.empty:
        st.info("Không đủ dữ liệu.")
    else:
        mel = grp.reset_index().melt(id_vars=dim, var_name='sentiment', value_name='count')
        fig = px.bar(
            mel,
            x=dim, y='count', color='sentiment', barmode='stack',
            title=f"{dim.title()} ↔ Cảm xúc",
            color_discrete_map=sentiment_colors
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- Section 4: Trend với màu cố định ---
    st.markdown("---")
    st.subheader("📈 Khuynh hướng Khía cạnh theo Học kỳ")
    with st.expander("Bộ lọc cho trend"):
        tr_course = st.selectbox("Môn", ["Tất cả"] + courses_all, key="tr_course")
        tr_cla    = st.selectbox("Lớp", ["Tất cả"] + classes_all,     key="tr_cla")
    asp_tr = st.selectbox("Chọn khía cạnh (trend)", aspects_all, key="tr_asp")

    df3 = df_full.copy()
    if tr_course != "Tất cả": df3 = df3[df3['course'] == tr_course]
    if tr_cla   != "Tất cả": df3 = df3[df3['class']  == tr_cla]
    df_tr = df3[df3['aspect'] == asp_tr]

    if df_tr.empty:
        st.info("Không đủ dữ liệu trend.")
    else:
        trend = df_tr.groupby(['semester', 'sentiment']).size().unstack(fill_value=0).reset_index()
        if trend.shape[0] > 1:
            # melt thành long form để dễ map màu
            trend_melt = trend.melt(id_vars='semester', var_name='sentiment', value_name='count')
            fig = px.line(
                trend_melt,
                x='semester', y='count', color='sentiment', markers=True,
                title=f"Khuynh hướng cảm xúc – {asp_tr}",
                color_discrete_map=sentiment_colors
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Không đủ kỳ để vẽ trend.")
