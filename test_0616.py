from datetime import datetime, time
import pandas as pd
import streamlit as st

st.header("アルバイトシフト管理システム")

if "shifts" not in st.session_state:
    st.session_state.shifts = []

# サイドバーに時給設定と給与合計を表示する
st.sidebar.header("給与設定")
hourly_wage = st.sidebar.number_input(
    label="時給を入力してください（円）",
    min_value=0,
    value=1100,  # 初期値
    step=10,
)

name = st.text_input(
    label="アルバイト先を入力してください",
    value="",
    help="あなたが働いているアルバイト先の名前を入力してください",
    placeholder="例: スタバ",
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

            # 登録時は「金額」ではなく「労働時間」だけを保存する（時給変更に対応するため）
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
    # データをデータフレームに変換
    df = pd.DataFrame(st.session_state.shifts)

    # 時給が変わってもリアルタイムに計算できるように修正
    df["見込み給与(円)"] = (df["労働時間(h)"] * hourly_wage).astype(int)

    # サイドバーに合計金額を表示
    total_pay = df["見込み給与(円)"].sum()
    total_hours = df["労働時間(h)"].sum()
    st.sidebar.metric(label="合計勤務時間", value=f"{total_hours:.1f} 時間")
    st.sidebar.metric(label="合計見込み給与", value=f"{total_pay:,} 円")

    # 表示形式を整える
    df_display = df.copy()
    df_display["日付"] = df_display["日付"].apply(lambda x: x.strftime("%Y/%m/%d"))
    df_display["開始"] = df_display["開始"].apply(lambda x: x.strftime("%H:%M"))
    df_display["終了"] = df_display["終了"].apply(lambda x: x.strftime("%H:%M"))
    df_display["見込み給与(円)"] = df_display["見込み給与(円)"].apply(
        lambda x: f"{x:,}"
    )

    # 1. 削除用のチェックボックス付きテーブルを表示（行選択機能）
    st.write("削除したいシフトにチェックを入れて、下の削除ボタンを押してください。")
    edited_df = st.data_editor(
        df_display,
        num_rows="fixed",
        use_container_width=True,
        disabled=["日付", "開始", "終了", "労働時間(h)", "見込み給与(円)"],  # 文字は編集不可にする
    )

    # 2. 削除ボタンの処理
    # data_editorでユーザーが行を選択・削除したイベントを取得
    col1, col2 = st.columns()
    with col1:
        # Streamlitの標準のごみ箱マークや行選択を使って消す、またはシンプルに全クリア
        if st.button("選択したシフトを削除", type="primary"):
            # 画面上で消されていない（残っている）行のインデックスだけを抽出して元データを更新
            remaining_indices = edited_df.index
            # 編集中のテーブルで行が削除されたかチェック
            if len(edited_df) < len(df_display):
                # 残ったデータだけをセッション状態に上書き保存
                st.session_state.shifts = [
                    st.session_state.shifts[i] for i in edited_df.index
                ]
                st.success("指定したシフトを削除しました")
                st.rerun()
            else:
                st.warning(
                    "表の左端の番号をクリックしてキーボードの「Delete」キーを押すか、行を削除してからボタンを押してください。"
                )

    with col2:
        if st.button("すべてのシフトをクリア"):
            st.session_state.shifts.clear()
            st.success("すべてのシフトをクリアしました")
            st.rerun()

else:
    st.info("登録されたシフトはまだありません。")
