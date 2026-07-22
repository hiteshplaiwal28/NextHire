import streamlit as st
from django.core.files.base import ContentFile

from jobs.models import Job
from ml_engine.parsers.pdf_parser import extract_text_from_pdf
from ml_engine.parsers.skill_extractor import extract_skills


def jobs_page():

    st.header("💼 Jobs")

    if "show_job_form" not in st.session_state:
        st.session_state.show_job_form = False

    if "edit_job" not in st.session_state:
        st.session_state.edit_job = None

    c1, c2 = st.columns([1, 5])

    with c1:

        if st.button("➕ Create Job"):

            st.session_state.show_job_form = True
            st.session_state.edit_job = None
            st.rerun()

    with c2:

        if st.session_state.show_job_form:

            if st.button("❌ Cancel"):

                st.session_state.show_job_form = False
                st.session_state.edit_job = None
                st.rerun()

    editing_job = None

    if st.session_state.edit_job:

        editing_job = Job.objects.get(
            id=st.session_state.edit_job
        )

    # =============================
    # Job Form
    # =============================

    if st.session_state.show_job_form:

        with st.form("job_form"):

            title = st.text_input(
                "Job Title",
                value=editing_job.title if editing_job else ""
            )

            department = st.text_input(
                "Department",
                value=editing_job.department if editing_job else ""
            )

            location = st.text_input(
                "Location",
                value=editing_job.location if editing_job else ""
            )

            experience = st.text_input(
                "Experience",
                value=editing_job.experience if editing_job else ""
            )

            education = st.text_input(
                "Education",
                value=editing_job.education if editing_job else ""
            )

            salary = st.text_input(
                "Salary",
                value=editing_job.salary if editing_job else ""
            )

            description = st.text_area(
                "Job Description",
                value=editing_job.description if editing_job else ""
            )

            jd_file = st.file_uploader(
                "Upload Job Description (PDF)",
                type=["pdf"]
            )

            submit = st.form_submit_button(
                "💾 Update Job" if editing_job else "✅ Create Job"
            )

            if submit:

                if editing_job:

                    job = editing_job

                else:

                    job = Job()

                    # Save recruiter only while creating
                    job.recruiter = st.session_state.user

                job.title = title
                job.department = department
                job.location = location
                job.experience = experience
                job.education = education
                job.salary = salary
                job.description = description

                if jd_file:

                    job.save()

                    job.jd_file.save(
                        jd_file.name,
                        ContentFile(jd_file.read())
                    )

                    text = extract_text_from_pdf(
                        job.jd_file.path
                    )

                    job.required_skills = extract_skills(text)

                job.save()

                st.success("✅ Job saved successfully!")

                st.session_state.show_job_form = False
                st.session_state.edit_job = None

                st.rerun()

    st.divider()

    st.subheader("📋 Current Jobs")

    # =============================
    # Show only logged-in user's jobs
    # =============================

    jobs = Job.objects.filter(
        recruiter=st.session_state.user
    ).order_by("-created_at")

    if not jobs.exists():

        st.info("No jobs found.")

        return

    for job in jobs:

        with st.container():

            st.subheader(f"📌 {job.title}")

            a, b, c = st.columns(3)

            a.write(f"**Department:** {job.department}")
            b.write(f"**Location:** {job.location}")
            c.write(f"**Status:** {job.status}")

            st.write(f"**Education:** {job.education}")
            st.write(f"**Experience:** {job.experience}")

            if job.salary:
                st.write(f"**Salary:** {job.salary}")

            st.write("**Description:**")
            st.write(job.description)

            st.write("**Required Skills:**")

            if job.required_skills:

                st.write(
                    ", ".join(job.required_skills)
                )

            else:

                st.write("No skills extracted.")

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✏ Edit",
                    key=f"edit_{job.id}"
                ):

                    st.session_state.edit_job = job.id
                    st.session_state.show_job_form = True
                    st.rerun()

            with col2:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{job.id}"
                ):

                    job.delete()

                    st.success(
                        "✅ Job deleted successfully!"
                    )

                    st.rerun()

            st.divider()