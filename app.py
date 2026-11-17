
import streamlit as st
import pandas as pd
import re
import html
from datetime import datetime
from io import BytesIO

from plagiarism import compare_documents

# PDF generation imports
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable
)


# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Plagiarism AI | Document Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# 2. PDF GENERATION FUNCTION
# ==================================================

def generate_pdf_report(
    score1,
    score2,
    status,
    status_message,
    common_words,
    matching_sentences,
    words1,
    words2
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=23,
        textColor=colors.HexColor("#293B70"),
        alignment=TA_CENTER,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#64748B"),
        alignment=TA_CENTER,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=colors.HexColor("#394B8A"),
        spaceBefore=15,
        spaceAfter=10
    )

    normal_style = ParagraphStyle(
        "CustomNormal",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        spaceAfter=6,
        wordWrap="CJK"
    )

    small_style = ParagraphStyle(
        "SmallText",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
        wordWrap="CJK"
    )

    story = []

    # TITLE

    story.append(
        Paragraph(
            "PLAGIARISM DETECTION SYSTEM",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Document Similarity Analysis Report",
            subtitle_style
        )
    )

    story.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
            subtitle_style
        )
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor("#A78BFA")
        )
    )

    # SIMILARITY RESULTS

    story.append(
        Paragraph("1. Similarity Analysis", heading_style)
    )

    similarity_data = [
        ["Algorithm", "Similarity Score"],
        ["Longest Common Subsequence (LCS)", f"{score1:.2f}%"],
        ["Jaccard Similarity", f"{score2:.2f}%"]
    ]

    similarity_table = Table(
        similarity_data,
        colWidths=[11 * cm, 5 * cm]
    )

    similarity_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.HexColor("#293B70")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 1), (-1, -1),
             colors.HexColor("#EEF2FF")),
            ("TEXTCOLOR", (0, 1), (-1, -1),
             colors.HexColor("#1E293B")),
            ("GRID", (0, 0), (-1, -1), 0.5,
             colors.HexColor("#CBD5E1")),
            ("PADDING", (0, 0), (-1, -1), 10),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
        ])
    )

    story.append(similarity_table)

    # DETECTION STATUS

    story.append(
        Paragraph("2. Detection Status", heading_style)
    )

    story.append(
        Paragraph(
            f"<b>{html.escape(status)}</b><br/>"
            f"{html.escape(status_message)}",
            normal_style
        )
    )

    # COMMON WORDS

    story.append(
        Paragraph("3. Common Words", heading_style)
    )

    story.append(
        Paragraph(
            f"Total common words: <b>{len(common_words)}</b>",
            normal_style
        )
    )

    if common_words:

        safe_words = html.escape(
            ", ".join(str(word) for word in common_words)
        )

        story.append(
            Paragraph(safe_words, normal_style)
        )

    else:

        story.append(
            Paragraph("No common words found.", normal_style)
        )

    # MATCHING SENTENCES

    story.append(
        Paragraph("4. Matching Sentence Detection", heading_style)
    )

    story.append(
        Paragraph(
            f"Total matching sentences: <b>{len(matching_sentences)}</b>",
            normal_style
        )
    )

    if matching_sentences:

        for index, sentence in enumerate(
            matching_sentences,
            start=1
        ):

            safe_sentence = html.escape(sentence)

            story.append(
                Paragraph(
                    f"<b>{index}.</b> {safe_sentence}",
                    normal_style
                )
            )

    else:

        story.append(
            Paragraph(
                "No exactly matching sentences found.",
                normal_style
            )
        )

    # DOCUMENT STATISTICS

    story.append(
        Paragraph("5. Document Statistics", heading_style)
    )

    statistics_data = [
        ["Document", "Total Words"],
        ["Document 01", str(words1)],
        ["Document 02", str(words2)]
    ]

    statistics_table = Table(
        statistics_data,
        colWidths=[11 * cm, 5 * cm]
    )

    statistics_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.HexColor("#293B70")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 1), (-1, -1),
             colors.HexColor("#EEF2FF")),
            ("GRID", (0, 0), (-1, -1), 0.5,
             colors.HexColor("#CBD5E1")),
            ("PADDING", (0, 0), (-1, -1), 10)
        ])
    )

    story.append(statistics_table)

    # DISCLAIMER

    story.append(Spacer(1, 25))

    story.append(
        HRFlowable(
            width="100%",
            thickness=0.5,
            color=colors.grey
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "<b>Note:</b> Similarity scores indicate textual overlap "
            "and do not prove plagiarism conclusively. "
            "The system uses string matching algorithms to "
            "compare document content.",
            small_style
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Generated using Python and Streamlit",
            subtitle_style
        )
    )

    # BUILD PDF

    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()


# ==================================================
# 3. SENTENCE MATCHING FUNCTION
# ==================================================

def find_matching_sentences(document1, document2):

    sentences1 = re.split(
        r'(?<=[.!?])\s+',
        document1.strip()
    )

    sentences2 = re.split(
        r'(?<=[.!?])\s+',
        document2.strip()
    )

    def clean_sentence(sentence):

        return re.sub(
            r'[^a-z0-9\s]',
            '',
            sentence.lower()
        ).strip()

    normalized2 = {
        clean_sentence(sentence)
        for sentence in sentences2
        if clean_sentence(sentence)
    }

    matching = []

    for sentence in sentences1:

        cleaned = clean_sentence(sentence)

        if cleaned and cleaned in normalized2:
            matching.append(sentence.strip())

    return list(dict.fromkeys(matching))


# ==================================================
# 4. CUSTOM DARK THEME
# ==================================================

st.markdown("""
<style>

.stApp {
    background-color: #0B1020;
    color: #E8ECF5;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    color: #F1F5FF !important;
    font-weight: 750 !important;
}

p, li {
    color: #C1CCE0;
}

[data-testid="stSidebar"] {
    background-color: #111A2D;
    border-right: 1px solid #293853;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #E8ECF5 !important;
}

.section-label {
    color: #A78BFA;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 10px;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #131D31;
    border: 1px solid #293853;
    border-radius: 16px;
}

.stTextArea label,
.stFileUploader label {
    color: #E0E7F5 !important;
    font-weight: 600 !important;
}

.stTextArea textarea {
    background-color: #0C1425 !important;
    color: white !important;
    border: 1px solid #35435F !important;
    border-radius: 10px !important;
}

[data-testid="stFileUploader"] {
    background-color: #0C1425;
    border: 1px dashed #53658B;
    border-radius: 12px;
    padding: 12px;
}

.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(90deg, #6D5CE8, #456CEB);
    color: white !important;
    border: none;
    border-radius: 11px;
    min-height: 48px;
    font-weight: 750;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: linear-gradient(90deg, #806FFF, #5286FF);
}

[data-testid="stMetric"] {
    background-color: #151F35;
    border: 1px solid #30405F;
    border-radius: 14px;
    padding: 22px;
}

[data-testid="stMetricLabel"] {
    color: #AAB8D0 !important;
}

[data-testid="stMetricValue"] {
    color: #A78BFA !important;
}

.stProgress > div > div > div {
    background-color: #8B5CF6 !important;
}

.match-card {
    background-color: #151F35;
    border: 1px solid #35435F;
    border-left: 4px solid #8B5CF6;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 12px;
    color: #E8ECF5;
}

hr {
    border-color: #293853 !important;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# 5. SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown("""
    <div style="padding:12px 0;">
        <h2 style="color:#A78BFA !important;">
            📄 PLAGIARISM AI
        </h2>
        <p style="color:#94A3B8 !important;">
            Document Intelligence System
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 🧠 Detection Algorithms")

    with st.expander("1. Naive String Matching"):
        st.write("Finds common words between two documents.")

    with st.expander("2. Longest Common Subsequence"):
        st.write("Identifies the longest common sequence of words.")

    with st.expander("3. Jaccard Similarity"):
        st.write("Measures similarity using common and unique words.")

    with st.expander("4. Sentence Matching"):
        st.write("Identifies exactly matching sentences in both documents.")

    st.divider()

    st.markdown("### ⚙️ How It Works")

    st.markdown("""
    1. Upload two documents.
    2. Extract document text.
    3. Compare document content.
    4. Apply matching algorithms.
    5. Detect matching sentences.
    6. Generate visual analysis.
    7. Download TXT or PDF report.
    """)

    st.divider()

    st.markdown("""
    <p style="color:#94A3B8; font-size:12px;">
        DEVELOPED USING<br>
        <b style="color:#C4B5FD;">
        PYTHON + STREAMLIT
        </b>
        <br><br>
        MINI PROJECT
    </p>
    """, unsafe_allow_html=True)


# ==================================================
# 6. MAIN BANNER
# ==================================================

st.html("""
<div style="
    background:linear-gradient(120deg,#191D3D,#292052,#12324E);
    padding:35px;
    border-radius:18px;
    border:1px solid #454475;
    margin-bottom:30px;
">

    <div style="
        color:#B5A5FF;
        font-size:12px;
        font-weight:800;
        letter-spacing:2px;
    ">
        AI POWERED TEXT ANALYSIS
    </div>

    <h1 style="
        color:#FFFFFF;
        font-size:36px;
        margin-top:12px;
        margin-bottom:12px;
    ">
        📄 Document Similarity Analyzer
    </h1>

    <p style="
        color:#C5CBE2;
        font-size:16px;
        margin-bottom:0;
    ">
        Detect textual similarities between documents
        using intelligent string matching algorithms.
    </p>

</div>
""")


# ==================================================
# 7. DOCUMENT INPUT
# ==================================================

st.markdown(
    '<div class="section-label">01 / DOCUMENT INPUT</div>',
    unsafe_allow_html=True
)

st.markdown("## Compare Your Documents")

st.write(
    "Upload two TXT files or paste their content "
    "to analyze their textual similarity."
)

col1, col2 = st.columns(2, gap="large")

with col1:

    with st.container(border=True):

        st.markdown("### 📘 Document 01")
        st.caption("Original document")

        file1 = st.file_uploader(
            "Upload first document",
            type=["txt"],
            key="file1"
        )

        text1 = st.text_area(
            "First document content",
            height=220,
            placeholder="Paste the original document text here...",
            key="text1"
        )


with col2:

    with st.container(border=True):

        st.markdown("### 📗 Document 02")
        st.caption("Document to compare")

        file2 = st.file_uploader(
            "Upload second document",
            type=["txt"],
            key="file2"
        )

        text2 = st.text_area(
            "Second document content",
            height=220,
            placeholder="Paste the document you want to check here...",
            key="text2"
        )


# ==================================================
# 8. ANALYZE BUTTON
# ==================================================

st.write("")

compare_button = st.button(
    "🔍 ANALYZE DOCUMENTS",
    use_container_width=True
)


# ==================================================
# 9. DOCUMENT ANALYSIS
# ==================================================

if compare_button:

    if file1 is not None:

        text1 = file1.getvalue().decode(
            "utf-8-sig",
            errors="replace"
        )

    if file2 is not None:

        text2 = file2.getvalue().decode(
            "utf-8-sig",
            errors="replace"
        )

    if not text1.strip() or not text2.strip():

        st.warning(
            "Please upload or enter content for both documents."
        )

    else:

        try:

            # EXISTING BACKEND FUNCTION

            result = compare_documents(text1, text2)

            score1 = float(result["lcs_similarity"])
            score2 = float(result["jaccard_similarity"])

            common_words = result["common_words"]

            matching_sentences = find_matching_sentences(
                text1,
                text2
            )

            words1 = len(text1.split())
            words2 = len(text2.split())

            # DETECTION STATUS

            if score1 >= 70:

                status = "HIGH SIMILARITY"

                status_message = (
                    "Significant textual overlap detected."
                )

            elif score1 >= 40:

                status = "MODERATE SIMILARITY"

                status_message = (
                    "Some textual overlap detected."
                )

            else:

                status = "LOW SIMILARITY"

                status_message = (
                    "Limited textual overlap detected."
                )

            # ==================================================
            # 10. SIMILARITY RESULTS
            # ==================================================

            st.divider()

            st.markdown(
                '<div class="section-label">'
                '02 / ANALYSIS REPORT</div>',
                unsafe_allow_html=True
            )

            st.markdown("## 📊 Similarity Analysis Results")

            st.write(
                "Results calculated using your document "
                "comparison algorithms."
            )

            metric1, metric2 = st.columns(2, gap="large")

            with metric1:

                st.metric(
                    "LCS Similarity",
                    f"{score1:.2f}%"
                )

                st.progress(
                    min(max(score1 / 100, 0), 1)
                )

                st.caption("Longest Common Subsequence")

            with metric2:

                st.metric(
                    "Jaccard Similarity",
                    f"{score2:.2f}%"
                )

                st.progress(
                    min(max(score2 / 100, 0), 1)
                )

                st.caption("Jaccard Word Set Similarity")

            # ==================================================
            # 11. DETECTION STATUS
            # ==================================================

            st.write("")

            st.markdown("### 🔎 Detection Status")

            if score1 >= 70:

                st.error(f"{status} — {status_message}")

            elif score1 >= 40:

                st.warning(f"{status} — {status_message}")

            else:

                st.success(f"{status} — {status_message}")

            # ==================================================
            # 12. SIMILARITY COMPARISON CHART
            # ==================================================

            st.divider()

            st.markdown("## 📈 Similarity Comparison Chart")

            similarity_data = pd.DataFrame({
                "Algorithm": [
                    "LCS Similarity",
                    "Jaccard Similarity"
                ],
                "Percentage": [
                    score1,
                    score2
                ]
            })

            st.bar_chart(
                similarity_data,
                x="Algorithm",
                y="Percentage",
                y_label="Similarity (%)",
                x_label="Algorithm"
            )

            # ==================================================
            # 13. COMMON WORDS
            # ==================================================

            st.divider()

            st.markdown("## 📝 Common Words Found")

            if common_words:

                st.info(
                    f"{len(common_words)} common words identified."
                )

                for word in common_words:

                    st.write(f"• {word}")

            else:

                st.success("No common words were found.")

            # ==================================================
            # 14. MATCHING SENTENCES
            # ==================================================

            st.divider()

            st.markdown("## 🔍 Matching Sentence Detection")

            st.write(
                "The system checks for sentences that appear "
                "in both documents."
            )

            st.metric(
                "Matching Sentences",
                len(matching_sentences)
            )

            if matching_sentences:

                st.success(
                    "Matching sentences were found in both documents."
                )

                for index, sentence in enumerate(
                    matching_sentences,
                    start=1
                ):

                    safe_sentence = html.escape(sentence)

                    st.markdown(
                        f"""
                        <div class="match-card">
                            <b style="color:#A78BFA;">
                                MATCH {index}
                            </b>
                            <br><br>
                            {safe_sentence}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.info(
                    "No exactly matching sentences were found."
                )

            # ==================================================
            # 15. DOCUMENT STATISTICS
            # ==================================================

            st.divider()

            st.markdown("## 📑 Document Statistics")

            stat1, stat2, stat3 = st.columns(3)

            stat1.metric("Document 01 Words", words1)

            stat2.metric("Document 02 Words", words2)

            stat3.metric("Common Words", len(common_words))

            st.markdown("### 📊 Word Count Comparison")

            word_data = pd.DataFrame({
                "Document": [
                    "Document 01",
                    "Document 02"
                ],
                "Word Count": [
                    words1,
                    words2
                ]
            })

            st.bar_chart(
                word_data,
                x="Document",
                y="Word Count",
                y_label="Total Words",
                x_label="Documents"
            )

            # ==================================================
            # 16. TEXT REPORT GENERATION
            # ==================================================

            st.divider()

            st.markdown("## 📥 Download Analysis Reports")

            report = f"""
========================================
       PLAGIARISM DETECTION REPORT
========================================

Generated on:
{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}

1. SIMILARITY ANALYSIS
----------------------------------------

LCS Similarity       : {score1:.2f}%
Jaccard Similarity   : {score2:.2f}%

2. DETECTION STATUS
----------------------------------------

{status}
{status_message}

3. COMMON WORDS
----------------------------------------

Total Common Words: {len(common_words)}

{', '.join(str(word) for word in common_words)}

4. MATCHING SENTENCES
----------------------------------------

Total Matching Sentences: {len(matching_sentences)}

{chr(10).join(
    f"{index}. {sentence}"
    for index, sentence in enumerate(matching_sentences, 1)
) if matching_sentences else "No matching sentences found."}

5. DOCUMENT STATISTICS
----------------------------------------

Document 01 Word Count: {words1}
Document 02 Word Count: {words2}

========================================
             END OF REPORT
========================================

Note: Similarity scores indicate textual overlap
and do not prove plagiarism conclusively.
"""

            # GENERATE PDF

            pdf_report = generate_pdf_report(
                score1,
                score2,
                status,
                status_message,
                common_words,
                matching_sentences,
                words1,
                words2
            )

            # DOWNLOAD BUTTONS

            download_col1, download_col2 = st.columns(2)

            with download_col1:

                st.download_button(
                    label="⬇️ DOWNLOAD TXT REPORT",
                    data=report,
                    file_name="plagiarism_analysis_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            with download_col2:

                st.download_button(
                    label="📄 DOWNLOAD PDF REPORT",
                    data=pdf_report,
                    file_name="plagiarism_analysis_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            st.success(
                "Your TXT and PDF analysis reports are ready!"
            )

            # ==================================================
            # 17. DISCLAIMER
            # ==================================================

            st.divider()

            st.caption(
                "Note: Similarity scores indicate textual overlap. "
                "They do not prove plagiarism conclusively. "
                "Sentence matching identifies exact sentence "
                "matches after ignoring capitalization and punctuation."
            )

        except Exception as e:

            st.error(
                f"An error occurred during comparison: {e}"
            )


# ==================================================
# 18. FOOTER
# ==================================================

st.divider()

st.html("""
<div style="
    text-align:center;
    color:#8290A9;
    font-size:13px;
    padding:20px;
">

    PLAGIARISM DETECTION SYSTEM

    <br><br>

    Built with Python | Streamlit |
    String Matching Algorithms

</div>
""")
