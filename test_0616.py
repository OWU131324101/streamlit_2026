import streamlit as st
from datetime import datetime, time

st.header("アルバイトシフト管理システム")

if "shifts" not in st.session_state:
    st.session_state.shifts = []

name = st.text_input(
    label = "アルバイト先を入力してください",
    value = "",
    help="あなたが働いているアルバイト先の名前を入力してください",
    placeholder="例: スタバ"
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
    import pandas as pd
    
    df = pd.DataFrame(st.session_state.shifts)
    
    df["日付"] = df["日付"].apply(lambda x: x.strftime("%Y/%m/%d"))
    df["開始"] = df["開始"].apply(lambda x: x.strftime("%H:%M"))
    df["終了"] = df["終了"].apply(lambda x: x.strftime("%H:%M"))
    
    st.dataframe(df, use_container_width=True)
else:
    st.info("登録されたシフトはまだありません。")

