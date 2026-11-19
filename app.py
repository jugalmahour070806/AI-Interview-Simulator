
import streamlit as st
import io
import wave
import cv2
import numpy as np

# ---------------- MODULE IMPORTS ----------------

from text_to_speech import speak_text
from speech_to_text import convert_speech_to_text
from voice_analysis import analyze_answer
from answer_evaluation import evaluate_answer
from interviewer import questions, get_feedback_message
from posture_analysis import analyze_posture_image
from database import create_table, save_interview_result
from report_generator import generate_report, export_report


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="IntervAI",
    layout="wide"
)

create_table()


# ---------------- DARK THEME ----------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0b1020,#111a32,#171b3a);
    color: white;
}
[data-testid="stSidebar"] {
    background: #10182d;
}
h1,h2,h3,h4,p,label,span {
    color: white;
}
.hero {
    background: linear-gradient(110deg,#25256b,#174b83);
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #4355a5;
}
.module-card {
    background:#1b2742;
    border:1px solid #344563;
    border-radius:14px;
    padding:17px;
    min-height:120px;
}
.question-box {
    background:#202e4b;
    color:white;
    border:1px solid #52658b;
    border-left:5px solid #818cf8;
    padding:20px;
    border-radius:12px;
    font-size:19px;
    font-weight:bold;
}
.result-box {
    background:#1b3440;
    color:white;
    border:1px solid #287b69;
    padding:15px;
    border-radius:12px;
}
.stTextArea textarea, .stTextInput input {
    background:#202e4b !important;
    color:white !important;
    -webkit-text-fill-color:white !important;
}
.stSelectbox div[data-baseweb="select"] > div {
    background:#202e4b !important;
    color:white !important;
}
.stButton button {
    background:linear-gradient(90deg,#6655df,#2878d5) !important;
    color:white !important;
    border:0;
    border-radius:10px;
    padding:9px 18px;
}
.stTabs [data-baseweb="tab"] {
    background:#1b2742;
    color:white !important;
}
.stTabs [aria-selected="true"] {
    background:#344b78 !important;
}
div[data-testid="stAlert"] * {
    color:white !important;
    -webkit-text-fill-color:white !important;
}
div[data-testid="stMetric"] {
    background:#1b2742;
    border:1px solid #344563;
    padding:12px;
    border-radius:12px;
}
hr {
    border-color:#465675 !important;
}
div[data-testid="stAlert"] {
    background: #123b2d !important;
    border: 1px solid #22c55e !important;
    border-radius: 12px !important;
}
div[data-testid="stAlert"] > div,
div[data-testid="stAlert"] [role="alert"] {
    background: transparent !important;
    color: #ffffff !important;
}
div[data-testid="stAlert"] p {
    color: white !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------

if "question_no" not in st.session_state:
    st.session_state.question_no = 0

if "answers" not in st.session_state:
    st.session_state.answers = []


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.title("Interview Setup")

    name = st.text_input("Candidate Name", "Candidate")

    role = st.selectbox(
        "Select Job Role",
        list(questions.keys())
    )

    level = st.selectbox(
        "Experience Level",
        ["Fresher", "Beginner", "Intermediate"]
    )

    st.divider()

    if st.button("Reset Interview"):
        st.session_state.question_no = 0
        st.session_state.answers = []

        for key in list(st.session_state.keys()):
            if key.startswith("answer_") or key.startswith("audio_duration_"):
                del st.session_state[key]

        st.rerun()


# ---------------- DASHBOARD HEADER ----------------

st.markdown("""
<div class="hero">
<h1>IntervAI</h1>
<p>Smart Interview Practice and Performance Analysis</p>
</div>
""", unsafe_allow_html=True)

st.write(
    f"**Candidate:** {name} | "
    f"**Role:** {role} | "
    f"**Level:** {level}"
)


# ---------------- MODULE CARDS ----------------

cards = st.columns(4)

modules = [
    ("Voice Interviewer", "Voice-based interview practice"),
    ("Confidence Analysis", "Speaking pattern analysis"),
    ("Body Language", "Webcam face detection"),
    ("Answer Accuracy", "Technical keyword evaluation")
]

for col, (title, desc) in zip(cards, modules):
    with col:
        st.markdown(
            f"""
            <div class="module-card">
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.write("")


# ---------------- TABS ----------------

tab1, tab2, tab3, tab4 = st.tabs([
    "Voice Interview",
    "Confidence Analysis",
    "Body Language",
    "Answer Accuracy"
])


# ---------------- CURRENT QUESTION ----------------

current_questions = questions[role]

qno = st.session_state.question_no % len(current_questions)
question = current_questions[qno]

answer_key = f"answer_{st.session_state.question_no}"
duration_key = f"audio_duration_{st.session_state.question_no}"


# ==================================================
# TAB 1 - VOICE INTERVIEWER
# ==================================================

with tab1:

    st.subheader("AI Voice Interviewer")

    st.markdown(
        f"""
        <div class="question-box">
            QUESTION {qno + 1}: {question}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.button("🔊 Speak Question"):
        try:
            speak_text(question)
            st.success("Question spoken successfully!")
        except Exception as e:
            st.error(f"Voice error: {e}")

    st.divider()

    st.subheader("🎤 Record Your Answer")

    recorded_audio = st.audio_input(
        "Click to record your answer"
    )

    if recorded_audio is not None:

        st.audio(recorded_audio)

        # Audio duration calculation
        try:
            with wave.open(
                io.BytesIO(recorded_audio.getvalue()), "rb"
            ) as audio_info:

                audio_duration = (
                    audio_info.getnframes()
                    / audio_info.getframerate()
                )

            st.session_state[duration_key] = audio_duration

        except Exception:
            st.session_state[duration_key] = None

        # Speech-to-text module
        if st.button("Convert Voice to Text"):

            transcript = convert_speech_to_text(recorded_audio)

            if transcript and not transcript.startswith("Error:") and transcript != "Speech recognition service unavailable.":

                st.session_state[answer_key] = transcript

                st.success("Voice converted successfully!")

                st.rerun()

            elif transcript == "":
                st.warning(
                    "Voice clear nahi thi. Dobara record karein."
                )

            else:
                st.error(transcript)

    answer = st.text_area(
        "Your Answer",
        key=answer_key,
        placeholder="Type or convert your answer here.",
        height=130
    )

    col1, col2 = st.columns(2)

    # Submit Answer
    with col1:

        if st.button("✅ Submit Answer"):

            final_answer = st.session_state.get(
                answer_key, ""
            ).strip()

            if final_answer:

                # Calculate confidence score
                voice_result = analyze_answer(
                    final_answer,
                    st.session_state.get(duration_key)
                )

                # Calculate technical accuracy
                technical_result = evaluate_answer(
                    question,
                    final_answer
                )

                new_record = {
                    "question_no": st.session_state.question_no,
                    "question": question,
                    "answer": final_answer,
                    "role": role,
                    "audio_duration": st.session_state.get(duration_key),
                    "confidence_score": voice_result["confidence_score"],
                    "accuracy_score": technical_result["accuracy_score"]
                }

                existing = [
                    item for item in st.session_state.answers
                    if item["question_no"] == st.session_state.question_no
                ]

                if existing:

                    for item in st.session_state.answers:
                        if item["question_no"] == st.session_state.question_no:
                            item.update(new_record)

                else:
                    st.session_state.answers.append(new_record)

                # Save result in database
                try:
                    save_interview_result(
                        role,
                        question,
                        final_answer,
                        voice_result["confidence_score"],
                        technical_result["accuracy_score"]
                    )

                except Exception as e:
                    st.warning(
                        f"Database save failed: {e}"
                    )

                st.success("Answer submitted successfully!")

                st.info(get_feedback_message())

            else:
                st.warning("Please enter your answer first.")

    # Next Question
    with col2:

        if st.button("➡️ Next Question"):

            st.session_state.question_no += 1

            st.rerun()


# ==================================================
# TAB 2 - CONFIDENCE ANALYSIS
# ==================================================

with tab2:

    st.subheader("Confidence Analysis")

    if not st.session_state.answers:

        st.info("Submit an answer to see your analysis.")

    else:

        latest_record = st.session_state.answers[-1]

        latest = latest_record["answer"]

        audio_duration = latest_record.get("audio_duration")

        result = analyze_answer(
            latest,
            audio_duration
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Confidence Indicator",
            f"{result['confidence_score']}/100"
        )

        c2.metric(
            "Word Count",
            result["word_count"]
        )

        c3.metric(
            "Filler Words",
            result["filler_count"]
        )

        st.progress(
            result["confidence_score"] / 100
        )

        st.divider()

        # Speaking speed
        st.subheader("🗣️ Speaking Speed")

        if result["speaking_wpm"] is not None:

            st.metric(
                "Words Per Minute (WPM)",
                result["speaking_wpm"]
            )

            st.caption(
                "Practice target used by this prototype: "
                "100–160 words per minute."
            )

        else:

            st.info(
                "Speaking speed unavailable. "
                "Record your answer to calculate WPM."
            )

        # Sentence analysis
        st.subheader("📝 Sentence Analysis")

        s1, s2 = st.columns(2)

        sentence_count = result["sentence_count"]

        average_length = result.get(
            "average_sentence_length",
            round(result["word_count"] / sentence_count, 1)
            if sentence_count else 0
        )

        s1.metric(
            "Sentence Count",
            sentence_count
        )

        s2.metric(
            "Average Words per Sentence",
            average_length
        )

        # Suggestions
        st.subheader("💡 Improvement Suggestions")

        for suggestion in result["suggestions"]:
            st.write("•", suggestion)

        st.markdown(
            """
            <div class="result-box">
                This is a basic rule-based communication indicator.
                It is not a psychological measurement of confidence.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("**Latest Answer:**")
        st.write(latest)


# ==================================================
# TAB 3 - BODY LANGUAGE
# ==================================================

with tab3:

    st.subheader("Body Language & Posture Detection")

    st.write(
        "Capture a webcam image to check face visibility and framing."
    )

    camera_image = st.camera_input(
        "Take Webcam Picture"
    )

    if camera_image is not None:

        posture_result = analyze_posture_image(
            camera_image.getvalue()
        )

        if posture_result is None:

            st.error("Could not read webcam image.")

        else:

            st.image(
                posture_result["frame"],
                channels="BGR",
                caption="Face detection preview"
            )

            if not posture_result["face_detected"]:

                st.warning(
                    "Face not detected. Improve lighting and face the camera."
                )

            else:

                st.success("Face detected successfully!")

                if posture_result["centered"]:
                    st.success("Face is reasonably centered.")
                else:
                    st.warning("Move your face towards the center.")

            st.caption(
                "Prototype limitation: this checks face visibility "
                "and framing, not full-body posture or emotions."
            )


# ==================================================
# TAB 4 - ANSWER ACCURACY
# ==================================================

with tab4:

    st.subheader("Answer Accuracy & Technical Knowledge")

    if not st.session_state.answers:

        st.info("Submit an answer to see technical evaluation.")

    else:

        selected = st.session_state.answers[-1]

        result = evaluate_answer(
            selected["question"],
            selected["answer"]
        )

        score = result["accuracy_score"]

        st.metric(
            "Answer Accuracy",
            f"{score}%"
        )

        st.progress(score / 100)

        st.write("**Question:**")
        st.write(selected["question"])

        st.write("**Your Answer:**")
        st.write(selected["answer"])

        st.write("**✅ Matched Technical Concepts:**")

        if result["matched_keywords"]:
            st.success(", ".join(result["matched_keywords"]))
        else:
            st.warning("No expected keywords detected.")

        st.write("**📌 Missing Technical Concepts:**")

        if result["missing_keywords"]:
            st.info(", ".join(result["missing_keywords"]))
        else:
            st.success("All expected keywords detected!")

        st.write("**💡 Improvement Suggestions:**")

        for suggestion in result["suggestions"]:
            st.write("•", suggestion)

        st.caption(
            "This is a keyword-based prototype evaluation, "
            "not a complete AI judgement of correctness."
        )


# ==================================================
# INTERVIEW SUMMARY & REPORT
# ==================================================

report_result = generate_report(
    st.session_state.answers,
    role
)

if report_result:

    report_answers, report_summary = report_result

    pdf_file = export_report(
        report_answers,
        report_summary
    )

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_file,
        file_name="AI_Interview_Report.pdf",
        mime="application/pdf"
    )