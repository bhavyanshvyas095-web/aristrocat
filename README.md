# ⚖️ Aristocrat: Local-First Legal & Taxation Analysis SaaS

Aristocrat is a privacy-focused, local-first legal and taxation document analysis tool designed to help users quickly analyze contracts, compliance clauses, and tax documents without risking confidential data exposure to cloud LLMs.

---

## 🌟 Key Features

- **🔒 100% Local & Private:** Powered by Ollama (`llama3`), ensuring zero data leaves your local machine.
- **📄 Multi-Modal Input System:**
  - **Document Upload:** Supports PDF (`.pdf`), Word (`.docx`), and Text (`.txt`) files.
  - **Visual & Photo Inputs:** Select photos from gallery or upload images (`.png`, `.jpg`, `.jpeg`).
  - **Live Camera Snap:** Capture contract documents in real time using your webcam/camera.
  - **Direct Text Input:** Paste legal clauses directly into the interface.
- **⚡ Legal & Tax Analysis:** Automated contract risk identification, clause summarization, and tax implication breakdown.

---

## 🛠️ Tech Stack & Dependencies

- **Frontend / Framework:** [Streamlit](https://streamlit.io/)
- **Local AI Engine:** [Ollama](https://ollama.com/) (Llama 3 8B)
- **Document Processing:** `pypdf`, `python-docx`
- **OCR & Image Processing:** `Pillow`, `pytesseract`
- **Language:** Python 3.x

---

## 🚀 How to Run Locally

### 1. Prerequisites
Ensure you have [Ollama](https://ollama.com/) installed and the Llama 3 model pulled:
```bash
ollama pull llama3