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



if name:
    st.subheader(f"{name}の予定表")

for shift in st.session_state.shifts:
    st.write(
        f"{shift['日付']} "
        f"{shift['開始']} ～ {shift['終了']}"
    )
