import streamlit as st

from utils.pdf_parser import extract_text_from_pdf
from utils.analyzer import analyze_resume


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🤖 AI Resume–Job Description Analyzer")

st.write(
    "Upload a resume and provide a job description to get "
    "AI-powered skill matching and resume analysis."
)


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

col1, col2 = st.columns(2)


with col1:

    st.subheader("📋 Job Description")

    job_description = st.text_area(
        "Paste the complete job description",
        height=350,
        placeholder="""
Example:

We are looking for a Python Developer with experience in
FastAPI, REST APIs, PostgreSQL, Docker and AWS.

The candidate should have strong problem solving skills
and experience building scalable backend applications.
"""
    )


with col2:

    st.subheader("📄 Resume")

    resume_file = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"]
    )


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

analyze_button = st.button(
    "🚀 Analyze Resume",
    use_container_width=True
)


if analyze_button:

    if not job_description.strip():

        st.warning(
            "Please enter a Job Description."
        )

        st.stop()


    if resume_file is None:

        st.warning(
            "Please upload a Resume PDF."
        )

        st.stop()


    # --------------------------------------------------
    # PROCESSING
    # --------------------------------------------------

    with st.spinner(
        "Reading resume and analyzing candidate..."
    ):

        try:

            resume_text = extract_text_from_pdf(
                resume_file
            )

            if not resume_text:

                st.error(
                    "Could not extract text from the PDF."
                )

                st.stop()


            result = analyze_resume(
                job_description=job_description,
                resume_text=resume_text
            )


        except Exception as e:

            st.error(
                f"Something went wrong: {str(e)}"
            )

            st.stop()


    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------

    st.divider()

    st.header("📊 Resume Analysis")


    # --------------------------------------------------
    # SCORE
    # --------------------------------------------------

    score_col1, score_col2 = st.columns(
        [1, 3]
    )


    with score_col1:

        st.metric(
            "Overall Match",
            f"{result.overall_match_percentage:.0f}%"
        )


    with score_col2:

        st.progress(
            result.overall_match_percentage / 100
        )


    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    st.subheader("📝 Summary")

    st.write(
        result.summary
    )


    # --------------------------------------------------
    # SKILLS
    # --------------------------------------------------

    st.subheader("🛠️ Skill Analysis")


    for skill in result.skill_analysis:

        if skill.status == "Strong Match":

            st.success(
                f"✅ **{skill.skill}** — {skill.status}\n\n"
                f"{skill.evidence}"
            )

        elif skill.status == "Partial Match":

            st.warning(
                f"⚠️ **{skill.skill}** — {skill.status}\n\n"
                f"{skill.evidence}"
            )

        else:

            st.error(
                f"❌ **{skill.skill}** — {skill.status}\n\n"
                f"{skill.evidence}"
            )


    # --------------------------------------------------
    # MATCHED SKILLS
    # --------------------------------------------------

    st.subheader("✅ Matched Skills")

    if result.matched_skills:

        for skill in result.matched_skills:

            st.write(
                f"• {skill}"
            )

    else:

        st.write("No strong skill matches found.")


    # --------------------------------------------------
    # PARTIAL SKILLS
    # --------------------------------------------------

    st.subheader("⚠️ Partial Matches")

    if result.partial_skills:

        for skill in result.partial_skills:

            st.write(
                f"• {skill}"
            )

    else:

        st.write("No partial matches found.")


    # --------------------------------------------------
    # MISSING SKILLS
    # --------------------------------------------------

    st.subheader("❌ Missing Skills")

    if result.missing_skills:

        for skill in result.missing_skills:

            st.write(
                f"• {skill}"
            )

    else:

        st.success(
            "No major missing skills identified."
        )


    # --------------------------------------------------
    # STRENGTHS & WEAKNESSES
    # --------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.subheader("💪 Strengths")

        for strength in result.strengths:

            st.write(
                f"• {strength}"
            )


    with col2:

        st.subheader("⚠️ Weaknesses")

        for weakness in result.weaknesses:

            st.write(
                f"• {weakness}"
            )


    # --------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------

    st.subheader("💼 Experience Match")

    st.info(
        result.experience_match
    )


    # --------------------------------------------------
    # EDUCATION
    # --------------------------------------------------

    st.subheader("🎓 Education Match")

    st.info(
        result.education_match
    )


    # --------------------------------------------------
    # SUGGESTIONS
    # --------------------------------------------------

    st.subheader(
        "🚀 Improvement Suggestions"
    )

    for suggestion in result.improvement_suggestions:

        st.write(
            f"• {suggestion}"
        )


    # --------------------------------------------------
    # RAW JSON
    # --------------------------------------------------

    with st.expander(
        "🔍 View Structured JSON"
    ):

        st.json(
            result.model_dump()
        )