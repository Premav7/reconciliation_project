from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os
from datetime import datetime

import re
from reportlab.platypus import Paragraph, Spacer

def markdown_to_paragraphs(report_text, styles):
    story = []
    for line in report_text.split("\n"):
        if not line.strip():
            continue

        line = line.replace("**", "")

        if line.startswith("### "):
            story.append(Paragraph(line.replace("### ", ""), styles["CustomHeading"]))
        elif line.startswith("## "):
            story.append(Paragraph(line.replace("## ", ""), styles["CustomHeading"]))

        elif line.strip().startswith(("* ", "- ")):
            story.append(Paragraph("• " + line[2:].strip(), styles["CustomBody"]))

        else:
            clean_line = line.replace("*", "")
            story.append(Paragraph(clean_line, styles["CustomBody"]))

        story.append(Spacer(1, 6))

    return story


def save_report_to_pdf(report_text: str, filename: str = None) -> str:
    output_dir = os.path.join(os.getcwd(), "outputs")
    os.makedirs(output_dir, exist_ok=True)

    if not filename:
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"reconciliation_{today}.pdf"

    output_path = os.path.join(output_dir, filename)

    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=0.8*inch, rightMargin=0.8*inch,
        topMargin=0.8*inch, bottomMargin=0.8*inch
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CustomHeading", parent=styles["Heading2"], spaceAfter=12, fontSize=12, leading=14))
    styles.add(ParagraphStyle(name="CustomBody", parent=styles["Normal"], leading=14, spaceAfter=8, fontSize=10))

    # Convert Markdown-like text into styled story
    story = markdown_to_paragraphs(report_text, styles)

    doc.build(story)
    return output_path
