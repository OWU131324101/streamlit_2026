from datetime import datetime, time
import pandas as pd
import streamlit as st

st.header("アルバイトシフト管理システム")

if "shifts" not in st.session_state:
    st.session_state.shifts = []

name = st.text_input(
    label="アルバイト先を入力してください",
    value="",
    help="あなたが働いているアルバイト先の名前を入力してください",
    placeholder="例: スタバ",
)

st.subheader("給与設定")
hourly_wage = st.number_input(
    label="時給を入力してください（円）",
    min_value=0,
    value=1100,
    step=10,
)

with st.form("cafe_order"):
    date = st.date_input(
        label="日付を入力してください", value=datetime.now(), help="カレンダーから日付を選択"
    )

    time1 = st.time_input(
        label="開始時刻", value=time(12, 0), help="アルバイト開始時刻を選択"
    )

    time2 = st.time_input(
        label="終了時刻", value=time(12, 0), help="アルバイト終了時刻を選択"
    )

    submitted = st.form_submit_button("登録する")
    if submitted:
        dt1 = datetime.combine(date, time1)
        dt2 = datetime.combine(date, time2)

        if dt2 < dt1:
            st.error("終了時刻は開始時刻より後の時間を設定してください。")
        else:
            duration = dt2 - dt1
            hours = duration.total_seconds() / 3600

            st.session_state.shifts.append(
                {
                    "日付": date,
                    "開始": time1,
                    "終了": time2,
                    "労働時間(h)": round(hours, 2),
                }
            )
            st.success("シフトを登録しました")
            st.rerun()

if name:
    st.subheader(f"{name}の予定表")

if st.session_state.shifts:
    df = pd.DataFrame(st.session_state.shifts)

    df["見込み給与(円)"] = (df["労働時間(h)"] * hourly_wage).astype(int)

    total_pay = df["見込み給与(円)"].sum()
    total_hours = df["労働時間(h)"].sum()

    col_tot1, col_tot2 = st.columns(2)
    with col_tot1:
        st.metric(label="合計勤務時間", value=f"{total_hours:.1f} 時間")
    with col_tot2:
        st.metric(label="合計見込み給与", value=f"{total_pay:,} 円")

    df_display = df.copy()
    df_display["日付"] = df_display["日付"].apply(lambda x: x.strftime("%Y/%m/%d"))
    df_display["開始"] = df_display["開始"].apply(lambda x: x.strftime("%H:%M"))
    df_display["終了"] = df_display["終了"].apply(lambda x: x.strftime("%H:%M"))
    df_display["見込み給与(円)"] = df_display["見込み給与(円)"].apply(
        lambda x: f"{x:,}"
    )

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
