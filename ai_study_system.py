import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import random

st.set_page_config(page_title="AI Study System", layout="wide")

# --------------------------------------------------
# LEETCODE PROBLEM BANK
# --------------------------------------------------
leetcode_problems = [
    ("Two Sum", "https://leetcode.com/problems/two-sum/"),
    ("Best Time to Buy and Sell Stock", "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"),
    ("Contains Duplicate", "https://leetcode.com/problems/contains-duplicate/"),
    ("Maximum Subarray", "https://leetcode.com/problems/maximum-subarray/"),
    ("Product of Array Except Self", "https://leetcode.com/problems/product-of-array-except-self/"),
    ("Valid Parentheses", "https://leetcode.com/problems/valid-parentheses/"),
    ("Binary Search", "https://leetcode.com/problems/binary-search/"),
    ("Climbing Stairs", "https://leetcode.com/problems/climbing-stairs/"),
    ("Invert Binary Tree", "https://leetcode.com/problems/invert-binary-tree/"),
    ("Merge Intervals", "https://leetcode.com/problems/merge-intervals/")
]

# --------------------------------------------------
# 120-DAY CURRICULUM WITH LINKS
# --------------------------------------------------
def generate_curriculum():
    topics = [
        # Month 1 (DSA + ML + DL)
        ("Sliding Window", "https://www.youtube.com/watch?v=MK-NZ4hN7rs"),
        ("Two Pointers", "https://www.youtube.com/watch?v=jzZsG8n2R9A"),
        ("Hashing", "https://www.youtube.com/watch?v=KEs5UyBJ39g"),
        ("Recursion", "https://www.youtube.com/watch?v=IJDJ0kBx2LM"),
        ("Backtracking", "https://www.youtube.com/watch?v=Zq4upTEaQyM"),
        ("NumPy Basics", "https://www.kaggle.com/learn/numpy"),
        ("Pandas Basics", "https://www.kaggle.com/learn/pandas"),
        ("Data Visualization", "https://www.kaggle.com/learn/data-visualization"),
        ("Linear Regression", "https://www.kaggle.com/learn/intro-to-machine-learning"),
        ("Logistic Regression", "https://scikit-learn.org/stable/modules/linear_model.html"),
        ("Decision Trees", "https://scikit-learn.org/stable/modules/tree.html"),
        ("Neural Networks Intro", "https://www.youtube.com/watch?v=aircAruvnKk"),
        ("Backpropagation", "https://www.youtube.com/watch?v=Ilg3gGewQ5U"),
        ("Mini ML Project", "https://www.kaggle.com/datasets"),
        
        # Month 2 (Backend + Advanced DSA)
        ("Trees", "https://www.youtube.com/watch?v=oSWTXtMglKE"),
        ("Binary Search Trees", "https://www.youtube.com/watch?v=9Jry5-82I68"),
        ("Graphs", "https://www.youtube.com/watch?v=gXgEDyodOJU"),
        ("Dynamic Programming", "https://www.youtube.com/watch?v=oBt53YbR9Kk"),
        ("Flask Basics", "https://flask.palletsprojects.com/en/stable/tutorial/"),
        ("REST APIs", "https://restfulapi.net/"),
        ("FastAPI Intro", "https://fastapi.tiangolo.com/tutorial/"),
        ("CRUD APIs", "https://fastapi.tiangolo.com/tutorial/body/"),
        ("SQLite Basics", "https://www.sqlitetutorial.net/"),
        ("Backend Project", "https://github.com/tiangolo/full-stack-fastapi-postgresql"),
        
        # Month 3 (Deep Learning + Integration)
        ("CNN Basics", "https://www.youtube.com/watch?v=YRhxdVk_sIs"),
        ("Image Preprocessing", "https://www.tensorflow.org/tutorials/images/cnn"),
        ("Model Training", "https://www.tensorflow.org/tutorials/keras/classification"),
        ("Transfer Learning", "https://www.tensorflow.org/tutorials/images/transfer_learning"),
        ("Frontend Basics", "https://www.freecodecamp.org/learn/"),
        ("API Integration", "https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs"),
        ("AI Web App", "https://streamlit.io/gallery"),
        
        # Month 4 (RL + Deployment)
        ("RL Fundamentals", "https://www.youtube.com/watch?v=2pWv7GOvuf0"),
        ("Q-Learning", "https://www.youtube.com/watch?v=0iqz4tcKN58"),
        ("Simple RL Agent", "https://gymnasium.farama.org/"),
        ("System Design Basics", "https://www.youtube.com/watch?v=UzLMhqg3_Wc"),
        ("Model Deployment", "https://fastapi.tiangolo.com/deployment/"),
        ("Docker Basics", "https://www.youtube.com/watch?v=fqMOX6JJhGo"),
        ("Cloud Deployment", "https://docs.streamlit.io/streamlit-community-cloud"),
        ("Final AI Project", "https://github.com/")
    ]

    curriculum = []
    for day in range(120):
        topic, link = topics[day % len(topics)]

        curriculum.append({
            "day": day + 1,
            "topic": topic,
            "link": link,
            "tasks": [
                f"Concept: {topic}",
                "Practice exercises",
                "Solve DSA problems",
                "Project/API work",
                "Revision + notes"
            ]
        })
    return curriculum


curriculum = generate_curriculum()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "day" not in st.session_state:
    st.session_state.day = 0

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Normal"

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("🚀 AI Study System")

today = datetime.now().strftime("%d %b %Y")
st.subheader(f"Day {st.session_state.day + 1} • {today}")

current = curriculum[st.session_state.day]

st.markdown(f"### 🎯 Topic: {current['topic']}")
st.markdown(f"🔗 **Study Link:** [Open Material]({current['link']})")

# --------------------------------------------------
# DAILY TASKS
# --------------------------------------------------
st.markdown("## ⏱ 5-Hour Plan")
completed = 0

for i, task in enumerate(current["tasks"]):
    if st.checkbox(task, key=f"task_{i}"):
        completed += 1

progress = completed / 5
st.progress(progress)

# --------------------------------------------------
# AI DIFFICULTY
# --------------------------------------------------
if progress == 1.0:
    st.success("All tasks completed!")

    if st.session_state.difficulty == "Normal":
        st.session_state.difficulty = "Hard"
    elif st.session_state.difficulty == "Hard":
        st.session_state.difficulty = "Advanced"

    st.info(f"Difficulty increased to: {st.session_state.difficulty}")

    if st.button("Next Day"):
        st.session_state.day += 1
        st.experimental_rerun()

# --------------------------------------------------
# DSA AUTO PROBLEM GENERATOR
# --------------------------------------------------
st.markdown("## 🧠 DSA Problem Generator")

difficulty = st.session_state.difficulty
num_problems = 3 if difficulty == "Normal" else 5 if difficulty == "Hard" else 6

if st.button("Generate Problems"):
    selected = random.sample(leetcode_problems, min(num_problems, len(leetcode_problems)))
    for name, link in selected:
        st.write(f"🔗 [{name}]({link})")

# --------------------------------------------------
# GITHUB COMMIT TRACKER
# --------------------------------------------------
st.sidebar.title("📊 GitHub Progress")

github_user = st.sidebar.text_input("GitHub username")

if github_user:
    url = f"https://api.github.com/users/{github_user}/events"
    response = requests.get(url)

    if response.status_code == 200:
        events = response.json()
        commits = sum(1 for e in events if e["type"] == "PushEvent")
        st.sidebar.metric("Recent commits", commits)
    else:
        st.sidebar.error("User not found")

# --------------------------------------------------
# OVERALL PROGRESS
# --------------------------------------------------
st.sidebar.title("📈 Study Progress")

days_done = st.session_state.day
progress_percent = (days_done / 120) * 100

st.sidebar.metric("Days completed", days_done)
st.sidebar.metric("Overall progress", f"{progress_percent:.1f}%")
st.sidebar.metric("Difficulty", st.session_state.difficulty)
