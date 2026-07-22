import streamlit as st
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from jobs.models import Job
from resumes.models import Resume


def dashboard_page():

    st.header("🏠 Dashboard")

    # ---------------------------------
    # Logged-in Recruiter
    # ---------------------------------

    recruiter = st.session_state.user

    # ---------------------------------
    # Fetch Recruiter's Data
    # ---------------------------------

    jobs = Job.objects.filter(
        recruiter=recruiter
    )

    resumes = Resume.objects.filter(
        recruiter=recruiter
    )

    # ---------------------------------
    # Dashboard Cards
    # ---------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "📄 Total Jobs",
            jobs.count()
        )

    with col2:

        st.metric(
            "👤 Total Candidates",
            resumes.count()
        )

    st.divider()

    # ---------------------------------
    # Recent Jobs
    # ---------------------------------

    st.subheader("📋 Recent Jobs")

    recent_jobs = jobs.order_by(
        "-created_at"
    )[:5]

    if recent_jobs.exists():

        for job in recent_jobs:

            st.write(
                f"• {job.title} ({job.location})"
            )

    else:

        st.info("No jobs available.")

    st.divider()

    # ---------------------------------
    # Recent Candidates
    # ---------------------------------

    st.subheader("👥 Recent Candidates")

    recent_candidates = resumes.order_by(
        "-uploaded_at"
    )[:5]

    if recent_candidates.exists():

        for candidate in recent_candidates:

            st.write(
                f"• {candidate.candidate_name}"
            )

    else:

        st.info("No candidates available.")