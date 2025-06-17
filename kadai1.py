import streamlit as st
import datetime
import time
from PIL import Image

# --- セッションステートの初期化 ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'done_tasks' not in st.session_state:
    st.session_state.done_tasks = []
if 'motivation_log' not in st.session_state:
    st.session_state.motivation_log = []
if 'study_records' not in st.session_state:
    st.session_state.study_records = []
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'custom_categories' not in st.session_state:
    st.session_state.custom_categories = []

st.title("学習プランナー🕊️💐")

# --- カテゴリ追加機能 ---
st.subheader("🗂️ 学習カテゴリ")
categories = ["基本情報技術者試験", "英語学習"]

st.markdown("#### 🔧 カテゴリを追加する")
new_category = st.text_input("新しいカテゴリ名を入力")
if st.button("カテゴリ追加"):
    if new_category and new_category not in st.session_state.custom_categories and new_category not in categories:
        st.session_state.custom_categories.append(new_category)
        st.success(f"「{new_category}」を追加しました！")
    elif new_category in st.session_state.custom_categories or new_category in categories:
        st.warning("そのカテゴリはすでに存在します")
    else:
        st.warning("カテゴリ名を入力してください")

# --- カテゴリ選択 ---
all_categories = categories + st.session_state.custom_categories
selected_category = st.selectbox("現在の学習カテゴリを選んでください", all_categories)

# --- タイマー機能 ---
st.subheader("⏱️ タイマー")
timer_placeholder = st.empty()

if st.session_state.start_time is None:
    if st.button("▶️ 学習開始"):
        st.session_state.start_time = time.time()
        st.experimental_rerun()
else:
    elapsed = int(time.time() - st.session_state.start_time)
    minutes = elapsed // 60
    seconds = elapsed % 60
    timer_placeholder.markdown(f"### 🕒 経過時間: {minutes:02d}:{seconds:02d}")

    if st.button("⏹️ 学習終了"):
        end_time = time.time()
        duration = round((end_time - st.session_state.start_time) / 60, 2)
        today = datetime.date.today().isoformat()
        st.session_state.study_records.append((today, selected_category, duration))
        st.success(f"{selected_category} に {duration} 分学習を記録しました！")
        st.session_state.start_time = None
        st.experimental_rerun()
    else:
        time.sleep(1)
        st.experimental_rerun()

# --- タスク入力エリア ---
st.subheader("🎯 タスク追加")
task = st.text_input("新しいタスクを入力してください")
if st.button("追加"):
    if task:
        st.session_state.tasks.append(task)
        st.success("タスクを追加しました！")
    else:
        st.warning("タスクを入力してください")

# --- タスク表示 ---
st.subheader("📝 タスクリスト")
left_col, right_col = st.columns(2)

with left_col:
    st.markdown("### ⏳ 未完了タスク")
    for i, t in enumerate(st.session_state.tasks):
        if st.checkbox(t, key=f"task_{i}"):
            st.session_state.done_tasks.append(t)
            st.session_state.tasks.pop(i)
            st.experimental_rerun()

with right_col:
    st.markdown("### ✅ 完了タスク")
    for dt in st.session_state.done_tasks:
        st.write(f"- {dt}")

# --- 学習記録の表示 ---
st.subheader("📚 学習時間の記録")
if st.session_state.study_records:
    for r in st.session_state.study_records:
        st.write(f"- {r[0]} | {r[1]} : {r[2]} 分")
else:
    st.info("まだ学習記録がありません")

st.subheader("🎯 今日の勉強目標")

goal_minutes = st.number_input("今日の目標勉強時間（分）を入力してください", min_value=1, step=5)

# 今日の勉強時間を合計
today = datetime.date.today().isoformat()
today_total = sum(r[2] for r in st.session_state.study_records if r[0] == today)

if goal_minutes:
    if today_total >= goal_minutes:
        st.image("happyrabbit.jpg", caption="目標達成！えらい！🐰✨", width=150)
    else:
        st.image("cryrabbit.jpg", caption="まだ足りないみたい…がんばろう！🐰💦", width=150)
