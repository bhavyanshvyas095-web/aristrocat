import streamlit as st
import ollama
from pypdf import PdfReader
import docx
from PIL import Image
import io

st.set_page_config(page_title="Aristocrat", page_icon="⚖️", layout="wide")

st.title("⚖️ Aristocrat: Your Personal Legal Assistant")
st.write("Upload legal documents, select photos from gallery, take a camera snap, or paste text directly for instant risk & tax analysis.")

# Sidebar for Input Mode Selection
st.sidebar.header("📌 Select Input Source")
input_option = st.sidebar.radio(
    "Choose Input Method:", 
    [
        "📄 Upload Documents (PDF / DOCX / TXT)", 
        "🖼️ Gallery Access (Upload Photos/Images)", 
        "📷 Camera Snap (Take Photo)", 
        "📝 Paste Text Directly"
    ]
)

contract_text = ""

# ---------------------------------------------------------
# 1. DOCUMENT UPLOAD (All PDF / DOCX / TXT Formats)
# ---------------------------------------------------------
if input_option == "📄 Upload Documents (PDF / DOCX / TXT)":
    uploaded_file = st.file_uploader("Upload Legal Document", type=["pdf", "docx", "doc", "txt"])
    if uploaded_file is not None:
        file_ext = uploaded_file.name.split(".")[-1].lower()
        
        # Read TXT
        if file_ext == "txt":
            contract_text = str(uploaded_file.read(), "utf-8")
            
        # Read PDF
        elif file_ext == "pdf":
            pdf_reader = PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    contract_text += text + "\n"
                    
        # Read DOCX
        elif file_ext in ["docx", "doc"]:
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                if para.text:
                    contract_text += para.text + "\n"

        st.success(f"Document '{uploaded_file.name}' loaded successfully!")
        if contract_text.strip():
            with st.expander("Preview Extracted Document Text"):
                st.write(contract_text[:1000] + ("..." if len(contract_text) > 1000 else ""))

# ---------------------------------------------------------
# 2. GALLERY ACCESS (Photos, Screenshots, Scans)
# ---------------------------------------------------------
elif input_option == "🖼️ Gallery Access (Upload Photos/Images)":
    uploaded_image = st.file_uploader("Select Photo/Screenshot from Gallery", type=["png", "jpg", "jpeg", "webp"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Selected Image from Gallery", use_container_width=True)
        st.info("📷 Image captured/selected. Note: OCR functionality processes text from images.")
        # Optional: Ask user for brief manual description/text if OCR is not active
        contract_text = st.text_area("Add notes/text extracted from the image if needed:", height=150)

# ---------------------------------------------------------
# 3. CAMERA ACCESS (Take Live Photo)
# ---------------------------------------------------------
elif input_option == "📷 Camera Snap (Take Photo)":
    camera_file = st.camera_input("Take a photo of the physical document")
    if camera_file is not None:
        image = Image.open(camera_file)
        st.image(image, caption="Captured Camera Document", use_container_width=True)
        st.success("Photo captured successfully!")
        contract_text = st.text_area("Add notes/text extracted from the photo if needed:", height=150)

# ---------------------------------------------------------
# 4. DIRECT TEXT PASTE
# ---------------------------------------------------------
else:
    contract_text = st.text_area("Paste Legal Contract / Argument Clause Here:", height=250)

# ---------------------------------------------------------
# ANALYSIS BUTTON & OLLAMA EXECUTION
# ---------------------------------------------------------
st.divider()
if st.button("🔍 Analyze Contract Risks & Tax Implications", type="primary"):
    if not contract_text.strip() and input_option not in ["🖼️ Gallery Access (Upload Photos/Images)", "📷 Camera Snap (Take Photo)"]:
        st.warning("Please upload a document, capture an image, or paste text first!")
    else:
        with st.spinner("Analyzing with local Llama 3 model..."):
            try:
                # If user gave image/photo without extra text, pass a default request
                prompt_content = contract_text.strip() if contract_text.strip() else "Please perform general legal risk analysis on this document context."
                
                response = ollama.chat(
                    model='llama3',
                    messages=[
                        {
                            'role': 'system',
                            'content': (
                                "You are an expert Indian legal and corporate tax advisor. "
                                "Analyze the provided legal clause/document/text. "
                                "Highlight key risks, hidden liabilities, compliance requirements, "
                                "and relevant Indian tax implications clearly with structured bullet points."
                            )
                        },
                        {
                            'role': 'user',
                            'content': prompt_content
                        }
                    ]
                )
                
                st.success("Analysis Complete!")
                st.markdown("### 📋 Risk & Structural Insights:")
                st.write(response['message']['content'])
                
            except Exception as e:
                st.error(f"Error communicating with local AI model: {e}")
                