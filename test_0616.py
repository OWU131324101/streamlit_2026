from datetime import datetime, time
import pandas as pd
import streamlit as st

st.header("アルバイトシフト管理システム")

if "shifts" not in st.session_state:
    st.session_state.shifts = []

name = st.text_input(
    label = "アルバイト先を入力してください",
    value = "",
    help="あなたが働いているアルバイト先の名前を入力してください",
    placeholder="例: スタバ"
)

money = st.int_input(
    label = "時給を入力してください",
    value = "",
    help="あなたが働いているアルバイト先の時給",
    placeholder="例: 1200"
)

with st.form("cafe_order"):
    date = st.date_input(
        label = "日付を入力してください",
        value = datetime.now(),
        help = "カレンダーから日付を選択"
    )

    time1 = st.time_input(
        label = "開始時刻",
        value = time(12,0),
        help = "アルバイト開始時刻を選択"
    )

    time2 = st.time_input(
        label = "終了時刻",
        value = time(12,0),
        help = "アルバイト終了時刻を選択"
    )


    submitted = st.form_submit_button("登録する")
    if submitted:
        st.session_state.shifts.append({
            "日付": date,
            "開始": time1,
            "終了": time2
        })

        st.success("シフトを登録しました")


if st.session_state.shifts:
    df = pd.DataFrame(st.session_state.shifts)

    df_display = df.copy()
    df_display["日付"] = df_display["日付"].apply(lambda x: x.strftime("%Y/%m/%d"))
    df_display["開始"] = df_display["開始"].apply(lambda x: x.strftime("%H:%M"))
    df_display["終了"] = df_display["終了"].apply(lambda x: x.strftime("%H:%M"))

    st.dataframe(df_display, use_container_width=True)
    
    st.write("---")
    st.subheader("シフトの削除")

    col1, col2 = st.columns([2, 1])

    with col1:
        delete_index = st.selectbox(
            "削除する行の番号を選択してください",
            options=df_display.index,
            format_func=lambda x: f"行 {x}: {df_display.loc[x, '日付']} ({df_display.loc[x, '開始']}～)",
        )

    with col2:
        st.write("")
        st.write("")
        if st.button("選択したシフトを削除", type="primary"):
            st.session_state.shifts.pop(delete_index)
            st.success("指定したシフトを削除しました")
            st.rerun() 

    if st.button("すべてのシフトをクリア"):
        st.session_state.shifts.clear()
        st.success("すべてのシフトをクリアしました")
        st.rerun()

else:
    st.info("登録されたシフトはまだありません。")

