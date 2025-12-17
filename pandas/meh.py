from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics

# Register font
pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))

styles = getSampleStyleSheet()
styles["BodyText"].fontName = "HeiseiMin-W3"
styles["Title"].fontName = "HeiseiMin-W3"

output_path = "/Users/jash/python/pandas/bub_matching_engine.pdf"
doc = SimpleDocTemplate(output_path, pagesize=letter)
story = []

# Title
story.append(Paragraph("Bub Matching Engine — Scientific Architecture (Dual-Model)", styles["Title"]))
story.append(Spacer(1, 20))

# Section A
text_a = """
SECTION A — NARRATIVE STORY SIMILARITY ENGINE

1. Overview
The Narrative Similarity Engine models the semantic, emotional, and psychological structure of a user's expressed story.

2. Mathematical Model
Let x(t) be the narrative token sequence:
E_sem = f_sem(x)
E_aff = f_aff(x)
E_latent = f_latent(x)

Combined embedding:
E = W1*E_sem + W2*E_aff + W3*E_latent

Similarity:
S_narr(i,j) = 1 / (1 + ||E_i - E_j||_2)

Emotional distribution distance:
D_KL(P_aff_i || P_aff_j)

Final score:
S_total = α*S_narr + (1-α)*exp(-D_KL)

3. Pipeline
- Semantic Transformer
- Affect Mapping
- Latent VAE Embedding
- Fusion
- Similarity Scoring
"""
story.append(Paragraph(text_a.replace("\n", "<br/>"), styles["BodyText"]))
story.append(PageBreak())

# Section B
text_b = """
SECTION B — BEHAVIORAL STORY SIMILARITY ENGINE

1. Overview
Behavioral story similarity models multi-session emotional trajectories.

2. Latent Trait Modeling
p(θ | S) ∝ p(S | θ)p(θ)

3. Time-Series Alignment
Soft-DTW:
S_beh(i,j) = exp(-DTW_soft(H_i, H_j))

4. Final Matching Score
S_combined = β*S_beh + (1-β)*S_narr
"""
story.append(Paragraph(text_b.replace("\n", "<br/>"), styles["BodyText"]))

doc.build(story)
output_path

