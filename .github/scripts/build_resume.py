from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from xml.sax.saxutils import escape
import re

src = Path(".github/resume_source.md").read_text(encoding="utf-8")
out = Path("resume.pdf")
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Name", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=18, leading=21, textColor=colors.HexColor("#14213d"), alignment=1, spaceAfter=3))
styles.add(ParagraphStyle(name="Tag", parent=styles["Normal"], fontSize=8.5, leading=11, alignment=1, textColor=colors.HexColor("#334155"), spaceAfter=4))
styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=10, leading=12, textColor=colors.HexColor("#0f4c81"), spaceBefore=7, spaceAfter=3, keepWithNext=True))
styles.add(ParagraphStyle(name="H3x", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=8.6, leading=10.5, textColor=colors.HexColor("#14213d"), spaceBefore=4, spaceAfter=2, keepWithNext=True))
styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.1, leading=10.1, textColor=colors.HexColor("#202938"), spaceAfter=3))
styles.add(ParagraphStyle(name="Bulletx", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.9, leading=9.7, leftIndent=10, firstLineIndent=-7, textColor=colors.HexColor("#202938"), spaceAfter=2))
def inline(s):
    s = escape(s)
    s = re.sub(r"\\[([^\\]]+)\\]\\((https?://[^)]+|mailto:[^)]+)\\)", r'<link href="\\2" color="#0f4c81"><u>\\1</u></link>', s)
    return re.sub(r"\\*\\*(.+?)\\*\\*", r"<b>\\1</b>", s)
story=[]
for raw in src.splitlines():
    line=raw.strip()
    if not line:
        story.append(Spacer(1,2)); continue
    if line.startswith("# "):
        story.append(Paragraph(escape(line[2:]), styles["Name"]))
    elif line.startswith("## "):
        story.append(Paragraph(escape(line[3:]), styles["H2x"]))
    elif line.startswith("### "):
        story.append(Paragraph(escape(line[4:]), styles["H3x"]))
    elif line.startswith("- "):
        story.append(Paragraph("• "+inline(line[2:]), styles["Bulletx"]))
    else:
        story.append(Paragraph(inline(line), styles["Tag"] if "Senior Technical Writer |" in line or "+91-" in line else styles["Bodyx"]))
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica",7)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(.62*inch,.28*inch,"Azariah Onyx | Senior Technical Writer")
    canvas.drawRightString(7.88*inch,.28*inch,str(doc.page))
    canvas.restoreState()
doc=SimpleDocTemplate(str(out),pagesize=letter,rightMargin=.62*inch,leftMargin=.62*inch,topMargin=.48*inch,bottomMargin=.48*inch)
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(f"Created {out} ({out.stat().st_size} bytes)")
