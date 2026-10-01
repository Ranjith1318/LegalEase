import os
import requests
import streamlit as st
from dotenv import load_dotenv
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.exporters import format_docx, format_pdf

load_dotenv()

DEFAULT_BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")

st.write(
    "Create professional legal document drafts using Generative AI."
)

# ---------------- SIDEBAR ----------------

st.sidebar.header("Settings")

backend_url = st.sidebar.text_input(
    "Backend URL",
    value=DEFAULT_BACKEND_URL
)

jurisdiction = st.sidebar.text_input(
    "Jurisdiction",
    value="India"
)

st.sidebar.markdown("---")

st.sidebar.info(
    "LegalEase generates draft documents for educational "
    "and productivity purposes. Review documents with a "
    "qualified legal professional before using them."
)

# ---------------- DOCUMENT INPUT ----------------

st.header("Create Your Document")

document_type = st.selectbox(
    "Document Type",
    [
        "Non-Disclosure Agreement",
        "Employment Agreement",
        "Lease Agreement",
        "Service Agreement",
        "Freelance Agreement",
        "Partnership Agreement",
        "Other"
    ]
)

parties = st.text_area(
    "Parties",
    placeholder=(
        "Example:\n"
        "Party A: ABC Technologies Pvt Ltd\n"
        "Party B: John Doe"
    ),
    height=120
)

terms = st.text_area(
    "Key Terms",
    placeholder=(
        "Example:\n"
        "Confidential information\n"
        "Non-disclosure obligation\n"
        "Duration of 2 years\n"
        "Payment terms"
    ),
    height=150
)

effective_date = st.text_input(
    "Effective Date",
    placeholder="01 October 2026"
)

instructions = st.text_area(
    "Additional Instructions",
    placeholder=(
        "Example: Create a professional, "
        "clear and easy-to-read legal document."
    ),
    height=100
)

# ---------------- GENERATE ----------------

if st.button("🚀 Generate Document", type="primary"):

    if not parties.strip():
        st.error("Please enter the parties.")
        st.stop()

    if not terms.strip():
        st.error("Please enter the key terms.")
        st.stop()

    payload = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "effective_date": effective_date,
        "jurisdiction": jurisdiction,
        "instructions": instructions
    }

    try:
        with st.spinner("Generating your legal document..."):

            response = requests.post(
                f"{backend_url.rstrip('/')}/generate",
                json=payload,
                timeout=120
            )

        if response.status_code == 200:

            result = response.json()
            document = result.get("document", "")

            st.session_state["document"] = document
            st.session_state["document_type"] = document_type

            st.success("✅ Document generated successfully!")

        else:
            st.error(
                f"Backend Error {response.status_code}: "
                f"{response.text}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Cannot connect to FastAPI backend. "
            "Make sure the backend server is running."
        )

    except requests.exceptions.Timeout:

        st.error(
            "❌ Request timed out. Please try again."
        )

    except Exception as e:

        st.error(f"❌ Error: {e}")

# ---------------- DOCUMENT PREVIEW ----------------

if "document" in st.session_state:

    st.markdown("---")

    st.header("📄 Generated Document")

    edited_document = st.text_area(
        "Edit your document",
        value=st.session_state["document"],
        height=600
    )

    st.session_state["document"] = edited_document

    # ---------------- DOWNLOAD ----------------

    st.markdown("### 📥 Download")

    col1, col2, col3 = st.columns(3)

    # TXT
    with col1:

        st.download_button(
            label="📄 Download TXT",
            data=edited_document,
            file_name="LegalEase_Document.txt",
            mime="text/plain"
        )

    # DOCX
    with col2:

        docx_file = format_docx(
            edited_document,
            st.session_state.get(
                "document_type",
                "Legal Document"
            )
        )

        st.download_button(
            label="📝 Download DOCX",
            data=docx_file,
            file_name="LegalEase_Document.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            )
        )

    # PDF
    with col3:

        pdf_file = format_pdf(
            edited_document,
            st.session_state.get(
                "document_type",
                "Legal Document"
            )
        )

        st.download_button(
            label="📕 Download PDF",
            data=pdf_file,
            file_name="LegalEase_Document.pdf",
            mime="application/pdf"
        )