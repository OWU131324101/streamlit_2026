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
    # 1. データをデータフレームに変換
    df = pd.DataFrame(st.session_state.shifts)

    # 表示形式を整える
    df_display = df.copy()
    df_display["日付"] = df_display["日付"].apply(lambda x: x.strftime("%Y/%m/%d"))
    df_display["開始"] = df_display["開始"].apply(lambda x: x.strftime("%H:%M"))
    df_display["終了"] = df_display["終了"].apply(lambda x: x.strftime("%H:%M"))

    # 表として表示
    st.dataframe(df_display, use_container_width=True)

    # 2. 削除機能の追加
    st.write("---")  # 区切り線
    st.subheader("シフトの削除")

    col1, col2 = st.columns([2, 1])

    with col1:
        # 削除したい行の番号（インデックス）を選択する
        delete_index = st.selectbox(
            "削除する行の番号を選択してください",
            options=df_display.index,
            format_func=lambda x: f"行 {x}: {df_display.loc[x, '日付']} ({df_display.loc[x, '開始']}～)",
        )

    with col2:
        # 縦位置を合わせるためのスペース
        st.write("")
        st.write("")
        # 選択した行を削除するボタン
        if st.button("選択したシフトを削除", type="primary"):
            st.session_state.shifts.pop(delete_index)
            st.success("指定したシフトを削除しました")
            st.rerun()  # 画面を更新

    # 3. 全削除ボタン（おまけ）
    if st.button("すべてのシフトをクリア"):
        st.session_state.shifts.clear()
        st.success("すべてのシフトをクリアしました")
        st.rerun()

else:
    st.info("登録されたシフトはまだありません。")

