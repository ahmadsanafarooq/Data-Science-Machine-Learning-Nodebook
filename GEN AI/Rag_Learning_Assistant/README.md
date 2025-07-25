# 🎓 RAG-Based Learning & Code Assistant with Evaluation

An advanced Retrieval-Augmented Generation (RAG) application that integrates **LangChain**, **Groq’s LLaMA 3**, **ChromaDB**, and **Gradio** to assist:

- 📚 **Students** — get smart help using uploaded learning materials
- 💻 **Developers** — ask questions based on documentation or code

⚡ Now includes **retrieval performance evaluation**, comparison to standard RAG setups, and real-world use case examples.

---

## ✨ Key Features

- 📂 Upload documents for contextual Q&A (PDF, TXT, MD, Code files)
- 💬 Chat with Learning or Code Assistant using Gradio UI
- 🧠 Powered by **Groq LLaMA 3** for lightning-fast, accurate responses
- 🧱 Vector store via **ChromaDB**, fallback to **TF-IDF**
- 🔍 NEW: Evaluate performance with precision, recall & MRR
- 📊 Benchmark tab for analyzing your retrieval pipeline

---

## 🧠 How It Works

1. Upload documents → chunked via LangChain
2. Text is embedded using HuggingFace (or TF-IDF fallback)
3. Stored persistently in ChromaDB (separately for each assistant)
4. When you ask a question:
   - Retrieves top-k relevant chunks
   - Sends query + context to **Groq LLaMA 3**
   - Answer is streamed via Gradio UI

---

## 📊 Retrieval Performance Evaluation

Evaluate your assistant’s retrieval quality using:

- ✅ **Precision@k**: Measures accuracy of top-k retrievals
- ✅ **Recall@k**: Measures how many relevant answers are retrieved
- ✅ **MRR** (Mean Reciprocal Rank): Measures ranking quality

🔁 Evaluation File Format (Upload as `.json`):
```json
[
  {
    "question": "What is overfitting in ML?",
    "keywords": ["overfitting", "training error"]
  },
  {
    "question": "Explain BFS vs DFS",
    "keywords": ["breadth", "depth", "graph"]
  }
]
```

📝 This file must be uploaded via the **Evaluation Bench** tab.

---

## 🔬 Comparison to Traditional RAG

| Feature              | This App             | Traditional RAG    |
|----------------------|----------------------|--------------------|
| Vector Store         | ChromaDB (persistent)| In-memory/None     |
| Evaluation Bench     | ✅ Yes               | ❌ No               |
| Assistant Modes      | Learning + Code      | Generic only       |
| TF-IDF Fallback      | ✅ Yes               | ❌ No               |
| Embedding Sources    | HuggingFace / TF-IDF | Usually HuggingFace|

---

## 🌍 Real-World Use Cases

- 👨‍🏫 Teachers uploading course syllabi for student Q&A
- 👩‍💻 Developers analyzing API docs to answer usage questions
- 📘 Students uploading textbooks or lecture notes for revision help
- 📈 Evaluating retrieval performance for different embedding models

---

## 🧰 Tech Stack

| Component      | Tool / Library                         |
|----------------|-----------------------------------------|
| LLM            | LLaMA 3 via [Groq API](https://console.groq.com/) |
| RAG Framework  | [LangChain](https://www.langchain.com/) |
| Embeddings     | HuggingFace models / TF-IDF fallback    |
| Vector Store   | [ChromaDB](https://www.trychroma.com/)  |
| Interface      | [Gradio](https://www.gradio.app/)       |
| Evaluation     | Scikit-learn + custom logic             |

---

## 📁 Project Structure

```
Rag_Learning_Assistant/
├── app.py                  # Main app
├── .env                    # API key file
├── chroma_learning_db/     # Chroma vector DB (learning)
├── chroma_code_db/         # Chroma vector DB (code)
├── evaluation/             # Sample JSON evaluation files
├── requirements.txt        # Dependencies
```

---

## ⚙️ Setup Instructions

### 1. Clone Repo
```bash
git clone https://github.com/ahmadsanafarooq/Data-Science-Machine-Learning-Nodebook.git
cd Data-Science-Machine-Learning-Nodebook/GEN\ AI/Rag_Learning_Assistant
```

### 2. Create Virtual Environment
```bash
python -m venv .env
source .env/bin/activate   # Windows: .env\Scripts\activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Set Groq API Key
```bash
echo "GROQ_API_KEY=your_key_here" > .env
```
Get a free key from: https://console.groq.com/

### 5. Launch the App
```bash
python app.py
```
Visit [http://localhost:7860](http://localhost:7860)

---

## 🖼️ Interface Overview

### 📚 Learning Tutor
- Upload `.pdf`, `.txt`, or `.md`
- Ask theory-based questions
- Receive rich, structured answers

### 💻 Code Assistant
- Upload `.py`, `.js`, `.json` files
- Ask code-related queries
- Get explanations, snippets, etc.

### 📊 Evaluation Bench
- Upload `.json` with questions/keywords
- Choose assistant mode
- View precision, recall, MRR, config summary

---

## 📎 Supported File Types

| Assistant        | Accepted File Types           |
|------------------|-------------------------------|
| Learning Tutor   | `.pdf`, `.txt`, `.md`         |
| Code Assistant   | `.py`, `.js`, `.json`         |
| Evaluation Bench | `.json`                       |

---

## 💬 Sample Queries

**Learning Tutor**  
> _"What is gradient descent in machine learning?"_

**Code Assistant**  
> _"What does this Flask route do in app.py?"_

---



Install via:
```bash
pip install -r requirements.txt
```

---

## 🛡 License

MIT License — free to use, modify, and distribute.

---

## 🙌 Credits

- 👨‍💻 Developed by [Ahmad Sana Farooq](https://github.com/ahmadsanafarooq)
- 💡 Powered by:
  - [LangChain](https://www.langchain.com/)
  - [Groq API](https://console.groq.com/)
  - [ChromaDB](https://www.trychroma.com/)
  - [Gradio](https://www.gradio.app/)
  - [HuggingFace Sentence Transformers](https://www.sbert.net/)

---

## 🔗 Connect

- 🌐 GitHub: [@ahmadsanafarooq](https://github.com/ahmadsanafarooq)
- 📄 LinkedIn: [LinkedIn Profile](https://www.linkedin.com/in/ahmad-sana-farooq/)
