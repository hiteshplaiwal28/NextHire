import streamlit as st

from jobs.models import Job
from resumes.models import Resume


def dashboard_page():

    st.header("🏠 Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("📄 Total Jobs", Job.objects.count())

    with col2:
        st.metric("👤 Total Candidates", Resume.objects.count())

    st.divider()

    st.subheader("📋 Recent Jobs")

    jobs = Job.objects.order_by("-created_at")[:5]

    if jobs:

        for job in jobs:
            st.write(f"• {job.title} ({job.location})")

    else:
        st.info("No jobs available.")