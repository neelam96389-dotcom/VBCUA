"""
app.py
Voice-Based Concept Understanding Analyser (VBCUA)
Main Streamlit application.
"""

import streamlit as st
import os

from speech_to_text import speech_to_text
from audio_utils import extract_audio_features, filler_word_ratio
from semantic_eval import REFERENCE_CONCEPTS, get_reference_text, compute_similarity
from scoring_engine import evaluate_understanding
from report_generator import generate_pdf_report

st.set_page_config(page_title="VBCUA", page_icon="🎙️", layout="wide")

UPLOAD_DIR = "uploads"
REPORT_DIR = "reports"

# Session state holds results across reruns (no database needed)
if "result" not in st.session_state:
    st.session_state.result = None

st.title("Voice-Based Concept Understanding Analyser")
st.caption("Automated evaluation of spoken conceptual explanations using AI.")

col_upload, col_reference = st.columns([2, 1])

with col_upload:
    st.subheader("Upload Student Audio (WAV)")
    audio_file = st.file_uploader("Drag and drop file here", type=["wav", "mp3"],
                                   label_visibility="collapsed")

with col_reference:
    concept_name = st.selectbox("Concept Reference", list(REFERENCE_CONCEPTS.keys()))
    st.info(get_reference_text(concept_name))

analyze_clicked = st.button("Analyze Concept Understanding", type="primary",
                             disabled=audio_file is None)

if analyze_clicked and audio_file:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    audio_path = os.path.join(UPLOAD_DIR, audio_file.name)
    with open(audio_path, "wb") as f:
        f.write(audio_file.getbuffer())

    with st.spinner("Processing and evaluating..."):
        transcript = speech_to_text(audio_path)

        waveform_path = os.path.join(REPORT_DIR, f"waveform_{audio_file.name}.png")
        audio_feats = extract_audio_features(audio_path, waveform_path)
        filler = filler_word_ratio(transcript)

        reference_text = get_reference_text(concept_name)
        similarity = compute_similarity(transcript, reference_text)

        evaluation = evaluate_understanding(similarity, filler, audio_feats)

    st.session_state.result = {
        "transcript": transcript,
        "reference_text": reference_text,
        "waveform_path": waveform_path,
        "similarity": similarity,
        "filler_ratio": filler,
        "pause_ratio": audio_feats["pause_ratio"],
        "rms_energy": audio_feats["rms_energy"],
        "final_score": evaluation["final_score"],
        "understanding_level": evaluation["understanding_level"],
        "audio_filename": audio_file.name,
    }

# ---------------- Results ----------------

result = st.session_state.result
if result:
    st.success("Analysis Completed")

    col1, col2, col3 = st.columns(3)
    col1.metric("Semantic Similarity", f"{result['similarity']}")
    col2.metric("Filler Word Ratio", f"{result['filler_ratio']}")
    col3.metric("Confidence (Energy)", f"{result['rms_energy']}")

    st.subheader("Reference Concept")
    st.write(result["reference_text"])

    st.subheader("Student Transcription")
    st.write(result["transcript"] or "_(no speech detected)_")

    st.subheader("Audio Visualization")
    if os.path.exists(result["waveform_path"]):
        st.image(result["waveform_path"])

    st.subheader("Evaluation Summary")
    st.table({
        "Metric": ["Semantic Similarity", "Filler Word Ratio", "Pause Ratio",
                   "Confidence (Energy)", "Final Score", "Understanding Level"],
        "Value": [result["similarity"], result["filler_ratio"], result["pause_ratio"],
                  result["rms_energy"], f"{result['final_score']}/100",
                  result["understanding_level"]],
    })

    pdf_path = os.path.join(REPORT_DIR, f"report_{result['audio_filename']}.pdf")
    generate_pdf_report(
        pdf_path, result["reference_text"], result["transcript"], result["waveform_path"],
        result["similarity"], result["filler_ratio"], result["pause_ratio"],
        result["rms_energy"], result["final_score"], result["understanding_level"],
    )

    with open(pdf_path, "rb") as f:
        st.download_button("Download PDF Report", f, file_name="VBCUA_Report.pdf")
