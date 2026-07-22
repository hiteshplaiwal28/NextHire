import os
import sys

import pandas as pd

# -----------------------------
# Connect Django
# -----------------------------
BASE_DIR = os.path.dirname(__file__)

sys.path.append(os.path.join(BASE_DIR, "backend"))
import streamlit as st
from app_pages.dashboard import dashboard_page
from app_pages.jobs import jobs_page
from app_pages.candidates import candidates_page



os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

import django
django.setup()

# -----------------------------
# Import Models
# -----------------------------
from accounts.views import login_user, register_user
from jobs.models import Job
from resumes.models import Resume
from ml_engine.matching.ranking import rank_candidates
from django.core.files.base import ContentFile

# -----------------------------
# Streamlit UI
# -----------------------------
if "show_job_form" not in st.session_state:
    st.session_state.show_job_form = False
    
st.set_page_config(
    page_title="NextHire",
    page_icon="🤖",
    layout="wide"
)
# -----------------------------
# Authentication
# -----------------------------

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:

    st.title("🤖 NextHire")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # -----------------------------
    # Login
    # -----------------------------

    with tab1:

        st.subheader("Login")

        username = st.text_input("Username", key="login_username")
        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login"):

            user = login_user(username, password)

            if user:

                st.session_state.user = user
                st.success("Login Successful!")
                st.rerun()

            else:

                st.error("Invalid Username or Password")

    # -----------------------------
    # Register
    # -----------------------------

    with tab2:

        st.subheader("Register")

        username = st.text_input("Username", key="register_username")
        email = st.text_input("Email", key="register_email")
        password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        if st.button("Create Account"):

            success, message = register_user(
                username,
                email,
                password
            )

            if success:
                st.success(message)
            else:
                st.error(message)

    st.stop()
st.sidebar.title("🤖 AI Recruitment")
st.sidebar.success(
    f"Logged in as: {st.session_state.user.username}"
)

if st.sidebar.button("🚪 Logout"):

    st.session_state.clear()

    st.rerun()
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Jobs",
        "Candidates",
        "AI Ranking",
    ]
)

st.title("AI Recruitment System")

if page == "Dashboard":

    dashboard_page()

elif page == "Jobs":
    jobs_page()
    
elif page == "Candidates":
    candidates_page()

    

elif page == "AI Ranking":

    st.header("🏆 AI Candidate Ranking")

    # ---------------------------------
    # Show only Recruiter's Jobs
    # ---------------------------------

    jobs = Job.objects.filter(
        recruiter=st.session_state.user
    )

    if not jobs.exists():

        st.warning("No jobs found.")

    else:

        selected_job = st.selectbox(
            "Select Job",
            jobs,
            format_func=lambda x: x.title
        )

        if st.button("Rank Candidates"):

            # ---------------------------------
            # Show only Recruiter's Candidates
            # ---------------------------------

            resumes = Resume.objects.filter(
                recruiter=st.session_state.user
            )

            rankings = rank_candidates(
                selected_job,
                resumes
            )

            if not rankings:

                st.warning("No candidates found.")

            else:

                data = []

                for rank, item in enumerate(rankings, start=1):

                    data.append({

                        "Rank": rank,

                        "Candidate":
                        item["candidate"].candidate_name,

                        "Final Score":
                        f'{item["score"]}/100',

                        "Skill Score":
                        f'{item["skill_score"]}/70',

                        "Education Score":
                        f'{item["education_score"]}/20',

                        "Experience Score":
                        f'{item["experience_score"]}/10',

                        "Matched Skills":
                        ", ".join(item["matched_skills"]),

                        "Missing Skills":
                        ", ".join(item["missing_skills"]),

                        "Email":
                        item["email"],

                        "Phone":
                        item["phone"],

                        "Resume Skills":
                        item["skills"],

                        "Education":
                        item["education"]

                    })

                st.subheader("📊 Ranking Results")

                st.dataframe(
                    pd.DataFrame(data),
                    use_container_width=True,
                    hide_index=True
                )

                # ---------------------------------
                # Shortlisted Candidates
                # ---------------------------------

                st.subheader("⭐ Shortlisted Candidates")

                shortlisted = [

                    item

                    for item in rankings

                    if item["score"] >= 30

                ]

                if shortlisted:

                    for item in shortlisted:

                        st.success(

                            f"👤 {item['candidate'].candidate_name}"

                            f" | ⭐ {item['score']}/100"

                        )

                    csv_data = []

                    for rank, item in enumerate(shortlisted, start=1):

                        csv_data.append({

                            "Rank": rank,

                            "Candidate":
                            item["candidate"].candidate_name,

                            "Email":
                            item["email"],

                            "Phone":
                            item["phone"],

                            "Final Score":
                            item["score"],

                            "Skill Score":
                            item["skill_score"],

                            "Education Score":
                            item["education_score"],

                            "Experience Score":
                            item["experience_score"],

                            "Matched Skills":
                            ", ".join(item["matched_skills"]),

                            "Missing Skills":
                            ", ".join(item["missing_skills"]),

                            "Resume Skills":
                            item["skills"],

                            "Education":
                            item["education"]

                        })

                    df = pd.DataFrame(csv_data)

                    st.download_button(

                        "📥 Download Shortlisted Candidates",

                        df.to_csv(index=False),

                        "shortlisted_candidates.csv",

                        "text/csv"

                    )

                else:

                    st.warning("No candidates shortlisted.")