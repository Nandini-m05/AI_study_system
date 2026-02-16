import streamlit as st
import pandas as pd
import requests
import random
from datetime import datetime
from openai import OpenAI

client = OpenAI()

st.set_page_config(page_title="AI Study System", layout="wide")

# --------------------------------------------------
# DSA PROBLEM BANK
# --------------------------------------------------
leetcode_problems = [
    ("Two Sum", "https://leetcode.com/problems/two-sum/"),
    ("Maximum Subarray", "https://leetcode.com/problems/maximum-subarray/"),
    ("Valid Parentheses", "https://leetcode.com/problems/valid-parentheses/"),
    ("Binary Search", "https://leetcode.com/problems/binary-search/"),
    ("Climbing Stairs", "https://leetcode.com/problems/climbing-stairs/"),
    ("Merge Intervals", "https://leetcode.com/problems/merge-intervals/"),
    ("Invert Binary Tree", "https://leetcode.com/problems/invert-binary-tree/"),
]

# --------------------------------------------------
# PHASE DEFINITIONS
# --------------------------------------------------
phases = [
    # Phase 1: Python + OOP + DSA
    {
        "name": "Python OOP + Core DSA",
        "days": 10,
        "topics": [
            ("Python OOP basics", "https://www.youtube.com/watch?v=JeznW_7DlB0"),
            ("Classes & objects", "https://www.youtube.com/watch?v=ZDa-Z5JzLYM"),
            ("Inheritance & polymorphism", "https://www.youtube.com/watch?v=RSl87lqOXDE"),
            ("Time complexity", "https://www.youtube.com/watch?v=0IAPZzGSbME"),
            ("Arrays", "https://www.youtube.com/watch?v=8hly31xKli0"),
            ("Strings", "https://www.youtube.com/watch?v=8wmn7k1TTcI"),
            ("Sliding window", "https://www.youtube.com/watch?v=MK-NZ4hN7rs"),
            ("Two pointers", "https://www.youtube.com/watch?v=jzZsG8n2R9A"),
            ("Hashing", "https://www.youtube.com/watch?v=KEs5UyBJ39g"),
            ("Recursion", "https://www.youtube.com/watch?v=IJDJ0kBx2LM"),
        ],
    },

    # Phase 2: ML
    {
        "name": "Machine Learning",
        "days": 10,
        "topics": [
            ("NumPy", "https://www.kaggle.com/learn/numpy"),
            ("Pandas", "https://www.kaggle.com/learn/pandas"),
            ("Visualization", "https://www.kaggle.com/learn/data-visualization"),
            ("ML basics", "https://www.kaggle.com/learn/intro-to-machine-learning"),
            ("Linear regression", "https://www.youtube.com/watch?v=3hZ_X7h1J9M"),
            ("Logistic regression", "https://www.youtube.com/watch?v=yIYKR4sgzI8"),
            ("Decision trees", "https://www.youtube.com/watch?v=7VeUPuFGJHk"),
            ("Model evaluation", "https://www.youtube.com/watch?v=85dtiMz9tSo"),
            ("Feature engineering", "https://www.youtube.com/watch?v=YJDLhYb3qDQ"),
            ("Mini ML project", "https://www.kaggle.com/datasets"),
        ],
    },

    # Phase 3: DL
    {
        "name": "Deep Learning",
        "days": 10,
        "topics": [
            ("Neural networks intro", "https://www.youtube.com/watch?v=aircAruvnKk"),
            ("Activation functions", "https://www.youtube.com/watch?v=m0pIlLfpXWE"),
            ("Backpropagation", "https://www.youtube.com/watch?v=Ilg3gGewQ5U"),
            ("TensorFlow basics", "https://www.tensorflow.org/tutorials"),
            ("CNN basics", "https://www.youtube.com/watch?v=YRhxdVk_sIs"),
            ("Image preprocessing", "https://www.tensorflow.org/tutorials/images/cnn"),
            ("Model training", "https://www.tensorflow.org/tutorials/keras/classification"),
            ("Regularization", "https://www.youtube.com/watch?v=Q81RR3yKn30"),
            ("Transfer learning", "https://www.tensorflow.org/tutorials/images/transfer_learning"),
            ("DL mini project", "https://www.tensorflow.org/tutorials"),
        ],
    },

    # Phase 4: RL
    {
        "name": "Reinforcement Learning",
        "days": 10,
        "topics": [
            ("RL fundamentals", "https://www.youtube.com/watch?v=2pWv7GOvuf0"),
            ("MDP", "https://www.youtube.com/watch?v=lfHX2hHRMVQ"),
            ("Q-learning", "https://www.youtube.com/watch?v=0iqz4tcKN58"),
            ("Exploration vs exploitation", "https://www.youtube.com/watch?v=mo96Nqlo1L8"),
            ("Policy learning", "https://www.youtube.com/watch?v=4dws0GvPjzk"),
            ("OpenAI Gym intro", "https://www.youtube.com/watch?v=Mut_u40Sqz4"),
            ("Simple RL agent", "https://gymnasium.farama.org/"),
            ("Reward tuning", "https://www.youtube.com/watch?v=GvR1D16kz8A"),
            ("RL experiment", "https://gymnasium.farama.org/"),
            ("RL mini project", "https://github.com/openai/gym"),
        ],
    },

    # Phase 5: Backend
    {
        "name": "Backend Development",
        "days": 10,
        "topics": [
            ("Flask basics", "https://flask.palletsprojects.com/en/stable/tutorial/"),
            ("Flask routing", "https://flask.palletsprojects.com/en/stable/quickstart/"),
            ("REST APIs", "https://restfulapi.net/"),
            ("Flask CRUD", "https://www.youtube.com/watch?v=Z1RJmh_OqeA"),
            ("FastAPI intro", "https://fastapi.tiangolo.com/tutorial/"),
            ("FastAPI routing", "https://fastapi.tiangolo.com/tutorial/path-params/"),
            ("Request models", "https://fastapi.tiangolo.com/tutorial/body/"),
            ("SQLite basics", "https://www.sqlitetutorial.net/"),
            ("Database integration", "https://fastapi.tiangolo.com/tutorial/sql-databases/"),
            ("Backend project", "https://github.com/tiangolo/full-stack-fastapi-postgresql"),
        ],
    },

    # Phase 6: Frontend
    {
        "name": "Frontend Development",
        "days": 10,
        "topics": [
            ("HTML basics", "https://www.freecodecamp.org/learn/"),
            ("CSS basics", "https://www.freecodecamp.org/learn/"),
            ("Flexbox", "https://www.freecodecamp.org/learn/"),
            ("Grid", "https://www.freecodecamp.org/learn/"),
            ("JavaScript basics", "https://javascript.info/"),
            ("DOM manipulation", "https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model"),
            ("Fetch API", "https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API"),
            ("Frontend project", "https://www.freecodecamp.org/learn/"),
            ("API integration", "https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs"),
            ("Full-stack integration", "https://streamlit.io/gallery"),
        ],
    },
]

# --------------------------------------------------
# CURRICULUM GENERATOR
# --------------------------------------------------
def generate_curriculum():
    curriculum = []
    day = 1

    for phase in phases:
        for i in range(phase["days"]):
            topic, link = phase["topics"][i]

            curriculum.append({
                "day": day,
                "phase": phase["name"],
                "topic": topic,
                "link": link,
                "tasks": [
                    f"Main concept: {topic}",
                    "Solve DSA problems",
                    "Implementation/practice",
                    "Project or integration",
                    "Revision + notes"
                ]
            })
            day += 1

    # Remaining days up to 120: advanced DSA + projects
    while day <= 120:
        curriculum.append({
            "day": day,
            "phase": "Advanced DSA + Projects",
            "topic": "Mixed DSA + Project refinement",
            "link": "https://neetcode.io/roadmap",
            "tasks": [
                "Solve 5–8 DSA problems",
                "Work on main project",
                "Optimize code",
                "Add features",
                "Revision"
            ]
        })
        day += 1

    return curriculum


curriculum = generate_curriculum()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "day" not in st.session_state:
    st.session_state.day = 0

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("🚀 AI Study System")

today = datetime.now().strftime("%d %b %Y")
current = curriculum[st.session_state.day]

st.subheader(f"Day {current['day']} • {today}")
st.markdown(f"### Phase: {current['phase']}")
st.markdown(f"### Topic: {current['topic']}")
st.markdown(f"🔗 [Study Material]({current['link']})")

# --------------------------------------------------
# TASKS
# --------------------------------------------------
st.markdown("## ⏱ 5-Hour Plan")
completed = 0

for i, task in enumerate(current["tasks"]):
    if st.checkbox(task, key=f"task_{i}"):
        completed += 1

progress = completed / 5
st.progress(progress)

if progress == 1.0:
    if st.button("Next Day"):
        st.session_state.day += 1
        st.experimental_rerun()

# --------------------------------------------------
# DSA GENERATOR
# --------------------------------------------------
st.markdown("## 🧠 DSA Problem Generator")

if st.button("Generate Problems"):
    selected = random.sample(leetcode_problems, 3)
    for name, link in selected:
        st.write(f"🔗 [{name}]({link})")

# --------------------------------------------------
# AI TUTOR
# --------------------------------------------------
st.markdown("## 🤖 AI Tutor")

problem_text = st.text_area("Describe the problem or doubt:")

if st.button("Get Help"):
    if problem_text:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{
                "role": "user",
                "content": f"Explain this problem clearly and give hints: {problem_text}"
            }]
        )
        st.write(response.choices[0].message.content)

