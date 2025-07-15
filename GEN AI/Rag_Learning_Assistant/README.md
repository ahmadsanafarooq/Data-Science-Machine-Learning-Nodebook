
# 🎓 RAG-Based Learning & Code Assistant

An intelligent Retrieval-Augmented Generation (RAG) application that uses **LangChain**, **Groq's LLaMA 3**, **ChromaDB**, and **Gradio** to assist:

- 📚 **Students** — get contextual help using uploaded learning materials.
- 💻 **Developers** — understand and query code documentation effectively.

With support for `.pdf`, `.txt`, `.md`, `.py`, `.js`, and `.json` files, this app enables you to interact with your documents through a sleek **Gradio** interface.

---

## ✨ Key Features

- 📂 Upload course materials or code documentation
- 🤖 Ask questions and get smart, context-aware responses
- 🧠 Powered by **LLaMA 3 (Groq API)** for fast, accurate answers
- 🧱 Uses **ChromaDB** for persistent document retrieval
- 🔄 Falls back to **TF-IDF** if transformer embeddings fail
- 💬 Dual chat tabs: **Learning Tutor** & **Code Helper**

---

## 🧠 How It Works

1. Upload your files → PDF, TXT, MD, code files.
2. Files are split into chunks using LangChain's text splitter.
3. Chunks are embedded using HuggingFace or TF-IDF (fallback).
4. Embeddings are stored in **ChromaDB**.
5. When you ask a question:
    - Top chunks are retrieved.
    - The query + context is sent to **LLaMA 3 via Groq API**.
    - A tailored answer is returned through Gradio.

---

## 🧰 Tech Stack

| Component      | Tool / Library                         |
|----------------|-----------------------------------------|
| LLM            | LLaMA 3 via [Groq API](https://console.groq.com/) |
| RAG Framework  | [LangChain](https://www.langchain.com/) |
| Embeddings     | HuggingFace models / TF-IDF fallback    |
| Vector Store   | [ChromaDB](https://www.trychroma.com/)  |
| Interface      | [Gradio](https://www.gradio.app/)       |
| Utilities      | Python, NumPy, Scikit-learn, dotenv     |

---

## 📁 Project Structure

```
Rag_Learning_Assistant/
├── app.py                  # Main application file
├── .env                    # Environment variables file (API key)
├── chroma_learning_db/     # Persistent vector DB for learning assistant
├── chroma_code_db/         # Persistent vector DB for code assistant
└── requirements.txt        # Python dependencies

```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ahmadsanafarooq/Data-Science-Machine-Learning-Nodebook.git
cd Data-Science-Machine-Learning-Nodebook/GEN\ AI/Rag_Learning_Assistant
```

### 2. Create Virtual Environment

```bash
python -m venv .env
source .env/bin/activate   # Windows: .env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up API Key

Create a `.env` file with your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

You can get a free key from: https://console.groq.com/

### 5. Run the Application

```bash
python app.py
```

App will launch at: [http://localhost:7860](http://localhost:7860)

---

## 🖼️ UI Overview

### 📚 Learning Tutor Tab

- Upload PDFs or notes
- Ask academic questions
- Get detailed, encouraging responses

### 💻 Code Documentation Helper Tab

- Upload code files or API docs
- Ask coding-related questions
- Get technical answers with code examples

---

## 🔧 Supported File Types

- `.pdf`, `.txt`, `.md` — for both assistants
- `.py`, `.js`, `.json` — for **Code Assistant** only

---

## 🧪 Example Queries

### Learning Tutor:
> _"Explain the bias-variance tradeoff in machine learning."_

→ Responds with a simplified explanation, examples, and source files.

### Code Assistant:
> _"How do I handle token-based authentication in this API?"_

→ Responds with relevant documentation snippets, code, and tips.

---

## 💡 Future Enhancements

- 🔒 User authentication and role-based access
- ☁️ Deployment to Hugging Face Spaces or Streamlit Cloud
- 📈 Add usage analytics and question logs
- 🧾 Support Word/Excel document ingestion

---

## ✅ Requirements

See `requirements.txt` (auto-generated from your `app.py`):

```txt
gradio
langchain
langchain-community
langchain-groq
langchain-huggingface
chromadb
python-dotenv
scikit-learn
numpy
PyPDF2
```

Install with:

```bash
pip install -r requirements.txt
```

---

## 🛡 License

This project is licensed under the **MIT License**.  
Feel free to use, modify, and contribute.

---

## 🙌 Credits

- 👨‍💻 Developed by [Ahmad Sana Farooq](https://github.com/ahmadsanafarooq)
- 🧠 Built using:
  - [LangChain](https://www.langchain.com/)
  - [Groq API](https://console.groq.com/)
  - [ChromaDB](https://www.trychroma.com/)
  - [Gradio](https://www.gradio.app/)
  - [HuggingFace Sentence Transformers](https://www.sbert.net/)

---

## 🔗 Connect

- 🌐 GitHub: [@ahmadsanafarooq](https://github.com/ahmadsanafarooq)
- 📄 LinkedIn: [LinkedIn Profile](https://www.linkedin.com/in/ahmadsanafarooq)

---
