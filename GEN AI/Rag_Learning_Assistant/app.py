import os
import gradio as gr
import json
import logging
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_groq import ChatGroq
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleEmbeddings:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=384, stop_words='english')
        self.fitted = False

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if not self.fitted:
            self.vectorizer.fit(texts)
            self.fitted = True
        embeddings = self.vectorizer.transform(texts)
        return embeddings.toarray().tolist()

    def embed_query(self, text: str) -> List[float]:
        if not self.fitted:
            return [0.0] * 384
        embedding = self.vectorizer.transform([text])
        return embedding.toarray()[0].tolist()


class RAGAssistant:
    def __init__(self, groq_api_key: str):
        self.groq_api_key = groq_api_key
        self.embeddings = self._init_embeddings()

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

        self.learning_vectorstore = None
        self.code_vectorstore = None

        self.llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama3-70b-8192",
            temperature=0.1
        )

        self.learning_persist_dir = "./chroma_learning_db"
        self.code_persist_dir = "./chroma_code_db"

        self._init_vector_stores()

    def _init_embeddings(self):
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            models_to_try = ["all-MiniLM-L6-v2", "paraphrase-MiniLM-L3-v2", "all-mpnet-base-v2"]
            for model_name in models_to_try:
                try:
                    embeddings = HuggingFaceEmbeddings(
                        model_name=model_name,
                        model_kwargs={'device': 'cpu'},
                        encode_kwargs={'normalize_embeddings': False}
                    )
                    return embeddings
                except Exception:
                    continue
        except ImportError:
            pass
        return SimpleEmbeddings()

    def _init_vector_stores(self):
        self.learning_vectorstore = Chroma(
            persist_directory=self.learning_persist_dir,
            embedding_function=self.embeddings,
            collection_name="learning_materials"
        )
        self.code_vectorstore = Chroma(
            persist_directory=self.code_persist_dir,
            embedding_function=self.embeddings,
            collection_name="code_documentation"
        )

    def load_documents(self, files: List[str], assistant_type: str) -> str:
        try:
            documents = []
            for file_path in files:
                if file_path.endswith('.pdf'):
                    loader = PyPDFLoader(file_path)
                else:
                    loader = TextLoader(file_path, encoding='utf-8')
                docs = loader.load()
                documents.extend(docs)

            if not documents:
                return "No documents could be loaded."

            chunks = self.text_splitter.split_documents(documents)
            for chunk in chunks:
                chunk.metadata['assistant_type'] = assistant_type

            if assistant_type == "learning":
                self.learning_vectorstore.add_documents(chunks)
                self.learning_vectorstore.persist()
            elif assistant_type == "code":
                self.code_vectorstore.add_documents(chunks)
                self.code_vectorstore.persist()

            return f"Loaded {len(chunks)} chunks from {len(documents)} documents."
        except Exception as e:
            return f"Error loading documents: {str(e)}"

    def get_learning_tutor_response(self, question: str) -> str:
        if not self.learning_vectorstore:
            return "Please upload some learning materials."
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.learning_vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True
        )
        result = qa_chain({"query": question})
        response = result['result']
        if result.get('source_documents'):
            response += "\n\n**Sources:**\n"
            for doc in result['source_documents'][:3]:
                response += f"- {Path(doc.metadata.get('source', 'Unknown')).name}\n"
        return response

    def get_code_helper_response(self, question: str) -> str:
        if not self.code_vectorstore:
            return "Please upload some code documentation."
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.code_vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True
        )
        result = qa_chain({"query": question})
        response = result['result']
        if result.get('source_documents'):
            response += "\n\n**Documentation Sources:**\n"
            for doc in result['source_documents'][:3]:
                response += f"- {Path(doc.metadata.get('source', 'Unknown')).name}\n"
        return response


# --- Evaluation Utilities ---
def evaluate_retrieval(assistant, assistant_type: str, eval_file: str, k=3):
    try:
        if not os.path.exists(eval_file):
            return f"Evaluation file {eval_file} not found."

        with open(eval_file, 'r', encoding='utf-8') as f:
            eval_data = json.load(f)

        total = len(eval_data)
        hits = 0
        mrr = 0

        for idx, item in enumerate(eval_data):
            question = item.get("question", "")
            keywords = item.get("keywords", [])
            result = assistant.get_learning_tutor_response(question) if assistant_type == "learning" else assistant.get_code_helper_response(question)
            hit = any(kw.lower() in result.lower() for kw in keywords)
            if hit:
                hits += 1
                mrr += 1 / (idx + 1)

        precision = hits / total if total else 0
        recall = precision
        mean_rr = mrr / total if total else 0

        return f"""
📊 Evaluation Summary ({assistant_type.title()} Assistant):
- Total Queries: {total}
- Precision@{k}: {precision:.2f}
- Recall@{k}: {recall:.2f}
- MRR: {mean_rr:.2f}

⚙️ Config:
- Retriever Top-K: {k}
- Embedding Model: {getattr(assistant.embeddings, 'model_name', 'TF-IDF (fallback)')}
- Vector Store: ChromaDB
        """
    except Exception as e:
        return f"Evaluation error: {str(e)}"


def create_gradio_interface(assistant: RAGAssistant):
    def upload_learning_files(files):
        return assistant.load_documents([f.name for f in files], "learning") if files else "No files uploaded."

    def upload_code_files(files):
        return assistant.load_documents([f.name for f in files], "code") if files else "No files uploaded."

    def learning_chat(message, history):
        if not message.strip():
            return history, ""
        response = assistant.get_learning_tutor_response(message)
        history.append((message, response))
        return history, ""

    def code_chat(message, history):
        if not message.strip():
            return history, ""
        response = assistant.get_code_helper_response(message)
        history.append((message, response))
        return history, ""

    with gr.Blocks(title="RAG-Based Learning & Code Assistant", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🎓 RAG-Based Learning & Code Assistant")

        with gr.Tabs():
            with gr.TabItem("📚 Learning Tutor"):
                learning_files = gr.File(file_types=[".pdf", ".txt", ".md"], file_count="multiple")
                learning_upload_btn = gr.Button("Upload Materials")
                learning_status = gr.Textbox()
                learning_chatbot = gr.Chatbot(height=400)
                learning_input = gr.Textbox(placeholder="Ask about your learning materials")
                learning_submit = gr.Button("Ask")

                learning_upload_btn.click(upload_learning_files, [learning_files], [learning_status])
                learning_submit.click(learning_chat, [learning_input, learning_chatbot], [learning_chatbot, learning_input])
                learning_input.submit(learning_chat, [learning_input, learning_chatbot], [learning_chatbot, learning_input])

            with gr.TabItem("💻 Code Documentation Helper"):
                code_files = gr.File(file_types=[".pdf", ".txt", ".md", ".py", ".js", ".json"], file_count="multiple")
                code_upload_btn = gr.Button("Upload Documentation")
                code_status = gr.Textbox()
                code_chatbot = gr.Chatbot(height=400)
                code_input = gr.Textbox(placeholder="Ask about your codebase or APIs")
                code_submit = gr.Button("Ask")

                code_upload_btn.click(upload_code_files, [code_files], [code_status])
                code_submit.click(code_chat, [code_input, code_chatbot], [code_chatbot, code_input])
                code_input.submit(code_chat, [code_input, code_chatbot], [code_chatbot, code_input])

            with gr.TabItem("📈 Evaluation Bench"):
                gr.Markdown("Upload a supported document (.json) containing evaluation questions and expected keywords.")
                eval_file_input = gr.File(file_types=[".json"], file_count="single")
                eval_assistant_choice = gr.Radio(["learning", "code"], label="Assistant", value="learning")
                eval_button = gr.Button("Run Evaluation")
                eval_output = gr.Textbox(lines=10)

                def run_eval(file, assistant_type):
                    if file is None:
                        return "Please upload a valid evaluation file."
                    return evaluate_retrieval(assistant, assistant_type, file.name)

                eval_button.click(run_eval, [eval_file_input, eval_assistant_choice], [eval_output])

    return demo


def main():
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("Set your GROQ_API_KEY in .env file")
        return
    assistant = RAGAssistant(groq_api_key)
    demo = create_gradio_interface(assistant)
    demo.launch(server_name="0.0.0.0", server_port=7860, debug=True)


if __name__ == "__main__":
    main()
