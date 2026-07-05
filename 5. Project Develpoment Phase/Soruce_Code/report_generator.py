"""
report_generator.py
Generates a structured PDF report: Reference Concept, Student Transcription,
Audio Visualization (waveform), and Evaluation Summary table.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors


def generate_pdf_report(output_path: str, reference_concept: str, transcript: str,
                         waveform_path: str, similarity: float, filler_ratio: float,
                         pause_ratio: float, rms_energy: float, final_score: int,
                         understanding_level: str) -> str:

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_path, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    elements = []

    elements.append(Paragraph("Voice-Based Concept Understanding Report", styles["Title"]))
    elements.append(Spacer(1, 0.4*cm))

    elements.append(Paragraph("Reference Concept", styles["Heading2"]))
    elements.append(Paragraph(reference_concept, styles["BodyText"]))
    elements.append(Spacer(1, 0.4*cm))

    elements.append(Paragraph("Student Transcription", styles["Heading2"]))
    elements.append(Paragraph(transcript or "(no speech detected)", styles["BodyText"]))
    elements.append(Spacer(1, 0.4*cm))

    if waveform_path and os.path.exists(waveform_path):
        elements.append(Paragraph("Audio Visualization", styles["Heading2"]))
        elements.append(Image(waveform_path, width=15*cm, height=4*cm))
        elements.append(Spacer(1, 0.4*cm))

    elements.append(Paragraph("Evaluation Summary", styles["Heading2"]))
    data = [
        ["Metric", "Value"],
        ["Semantic Similarity", f"{similarity}"],
        ["Filler Word Ratio", f"{filler_ratio}"],
        ["Pause Ratio", f"{pause_ratio}"],
        ["Confidence (Energy)", f"{rms_energy}"],
        ["Final Score", f"{final_score}/100"],
        ["Understanding Level", understanding_level],
    ]
    table = Table(data, colWidths=[8*cm, 7*cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F46E5")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(table)

    doc.build(elements)
    return output_path
