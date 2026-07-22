import os
import sys
import django
import streamlit as st

from django.core.files.base import ContentFile

# ---------------------------------
# Django Setup
# ---------------------------------

sys.path.append(
    os.path.join(os.path.dirname(__file__), "..", "backend")
)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from resumes.models import Resume

# ---------------------------------
# Candidates Page
# ---------------------------------


def candidates_page():

    st.header("👥 Candidates")

    # ==========================================
    # Upload Candidate
    # ==========================================

    st.subheader("➕ Add Candidate")

    uploaded_resume = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_resume is not None:

        if st.button("Upload Candidate"):

            try:

                # Create Resume for logged-in recruiter
                resume = Resume(
                    recruiter=st.session_state.user
                )

                resume.resume.save(
                    uploaded_resume.name,
                    ContentFile(uploaded_resume.read()),
                    save=False
                )

                resume.save()

                st.success("✅ Candidate uploaded successfully!")

                st.rerun()

            except Exception as e:

                st.error(f"Upload Failed : {e}")

    st.divider()

    # ==========================================
    # Show only logged-in recruiter's candidates
    # ==========================================

    resumes = Resume.objects.filter(
        recruiter=st.session_state.user
    ).order_by("-uploaded_at")

    st.metric(
        "Total Candidates",
        resumes.count()
    )

    st.divider()

    if not resumes.exists():

        st.info("No candidates found.")

        return

    # ==========================================
    # Candidate Cards
    # ==========================================

    for resume in resumes:

        with st.container():

            st.subheader(
                f"👤 {resume.candidate_name or 'Unknown Candidate'}"
            )

            st.write(
                f"📧 **Email:** {resume.email if resume.email else 'Not Provided'}"
            )

            st.write(
                f"📞 **Phone:** {resume.phone if resume.phone else 'Not Provided'}"
            )

            st.write("🛠 **Skills:**")

            if resume.skills:
                st.write(", ".join(resume.skills))
            else:
                st.write("Not Provided")

            st.write("🎓 **Education:**")

            if resume.education:

                if isinstance(resume.education, list):
                    st.write(", ".join(resume.education))
                else:
                    st.write(resume.education)

            else:
                st.write("Not Provided")

            st.write(
                f"💼 **Experience:** {resume.experience if resume.experience else 'Not Provided'}"
            )

            st.write(
                f"📅 Uploaded : {resume.uploaded_at.strftime('%d-%m-%Y')}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if resume.resume:

                    with open(resume.resume.path, "rb") as pdf:

                        st.download_button(
                            "⬇ Download Resume",
                            pdf.read(),
                            file_name=os.path.basename(
                                resume.resume.name
                            ),
                            mime="application/pdf",
                            key=f"download_{resume.id}"
                        )

            with col2:

                if st.button(
                    "🗑 Delete Candidate",
                    key=f"delete_{resume.id}"
                ):

                    if resume.resume:
                        resume.resume.delete(save=False)

                    resume.delete()

                    st.success(
                        "Candidate deleted successfully."
                    )

                    st.rerun()

            st.divider()