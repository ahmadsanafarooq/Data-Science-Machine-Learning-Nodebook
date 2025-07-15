import os
import gradio as gr
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.schema import Document
from pathlib import Path
from typing import List
import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleEmbeddings:
    """Simple TF-IDF based embeddings as fallback"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=384, stop_words='english')
        self.fitted = False
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents"""
        if not self.fitted:
            self.vectorizer.fit(texts)
            self.fitted = True
        
        embeddings = self.vectorizer.transform(texts)
        return embeddings.toarray().tolist()
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query"""
        if not self.fitted:
            # If not fitted, return zero vector
            return [0.0] * 384
        
        embedding = self.vectorizer.transform([text])
        return embedding.toarray()[0].tolist()

class RAGAssistant:
    def __init__(self, groq_api_key: str):
        """Initialize the RAG Assistant with Groq API key"""
        self.groq_api_key = groq_api_key
        
        # Initialize embeddings with fallback
        self.embeddings = self._init_embeddings()
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        # Initialize separate vector stores for each assistant
        self.learning_vectorstore = None
        self.code_vectorstore = None
        
        # Initialize LLM
        self.llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama3-70b-8192",
            temperature=0.1
        )
        
        # Create persistent directories
        self.learning_persist_dir = "./chroma_learning_db"
        self.code_persist_dir = "./chroma_code_db"
        
        # Initialize vector stores
        self._init_vector_stores()
    
    def _init_embeddings(self):
        """Initialize embeddings with multiple fallback options"""
        # Try HuggingFace first
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            print("Trying HuggingFace embeddings...")
            
            # Try different model names
            models_to_try = [
                "all-MiniLM-L6-v2",
                "paraphrase-MiniLM-L3-v2",
                "all-mpnet-base-v2"
            ]
            
            for model_name in models_to_try:
                try:
                    embeddings = HuggingFaceEmbeddings(
                        model_name=model_name,
                        model_kwargs={'device': 'cpu'},
                        encode_kwargs={'normalize_embeddings': False}
                    )
                    print(f"Successfully loaded HuggingFace model: {model_name}")
                    return embeddings
                except Exception as e:
                    print(f"Failed to load {model_name}: {e}")
                    continue
            
        except ImportError:
            print("HuggingFace embeddings not available")
        
        # Fallback to simple TF-IDF embeddings
        print("Using TF-IDF embeddings as fallback...")
        return SimpleEmbeddings()
    
    def _init_vector_stores(self):
        """Initialize ChromaDB vector stores"""
        try:
            # Learning Tutor vector store
            self.learning_vectorstore = Chroma(
                persist_directory=self.learning_persist_dir,
                embedding_function=self.embeddings,
                collection_name="learning_materials"
            )
            
            # Code Documentation vector store
            self.code_vectorstore = Chroma(
                persist_directory=self.code_persist_dir,
                embedding_function=self.embeddings,
                collection_name="code_documentation"
            )
            
        except Exception as e:
            logger.error(f"Error initializing vector stores: {str(e)}")
            raise
    
    def load_documents(self, files: List[str], assistant_type: str) -> str:
        """Load documents into the appropriate vector store"""
        try:
            documents = []
            
            for file_path in files:
                try:
                    if file_path.endswith('.pdf'):
                        loader = PyPDFLoader(file_path)
                    else:
                        loader = TextLoader(file_path, encoding='utf-8')
                    
                    docs = loader.load()
                    documents.extend(docs)
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
                    continue
            
            if not documents:
                return "No documents could be loaded. Please check your files."
            
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            # Add metadata to distinguish document types
            for chunk in chunks:
                chunk.metadata['assistant_type'] = assistant_type
            
            # Add to appropriate vector store
            if assistant_type == "learning":
                self.learning_vectorstore.add_documents(chunks)
                self.learning_vectorstore.persist()
            elif assistant_type == "code":
                self.code_vectorstore.add_documents(chunks)
                self.code_vectorstore.persist()
            
            return f"Successfully loaded {len(chunks)} chunks from {len(documents)} documents into {assistant_type} assistant."
            
        except Exception as e:
            logger.error(f"Error loading documents: {str(e)}")
            return f"Error loading documents: {str(e)}"
    
    def get_learning_tutor_response(self, question: str) -> str:
        """Get response from Learning Tutor"""
        try:
            if not self.learning_vectorstore:
                return "Please upload some learning materials first."
            
            # Create retrieval QA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.learning_vectorstore.as_retriever(
                    search_kwargs={"k": 3}
                ),
                return_source_documents=True
            )
            
            # Custom prompt for learning tutor
            learning_prompt = f"""
            You are an AI learning assistant that helps students understand academic concepts. 
            Based on the provided course materials, answer the student's question clearly and educationally.
            
            Guidelines:
            - Provide clear, educational explanations
            - Use examples when helpful
            - Reference specific sources when possible
            - Adapt to the student's level of understanding
            - Offer additional practice questions or related concepts when relevant
            - Maintain an encouraging, supportive tone
            
            Student's question: {question}
            
            Please provide a helpful, educational response:
            """
            
            result = qa_chain({"query": learning_prompt})
            
            # Format response with sources
            response = result['result']
            
            if result.get('source_documents'):
                response += "\n\n**Sources:**\n"
                for i, doc in enumerate(result['source_documents'][:3]):
                    source = doc.metadata.get('source', 'Unknown')
                    response += f"- {Path(source).name}\n"
            
            return response
            
        except Exception as e:
            logger.error(f"Error in learning tutor: {str(e)}")
            return f"Error generating response: {str(e)}"
    
    def get_code_helper_response(self, question: str) -> str:
        """Get response from Code Documentation Helper"""
        try:
            if not self.code_vectorstore:
                return "Please upload some code documentation first."
            
            # Create retrieval QA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.code_vectorstore.as_retriever(
                    search_kwargs={"k": 3}
                ),
                return_source_documents=True
            )
            
            # Custom prompt for code helper
            code_prompt = f"""
            You are a technical assistant that helps developers understand codebases and APIs.
            Based on the provided documentation and code examples, answer the developer's question.
            
            Guidelines:
            - Provide practical, actionable guidance
            - Include relevant code snippets with explanations
            - Reference specific documentation sections when possible
            - Highlight important considerations (security, performance, errors)
            - Suggest related APIs or patterns that might be useful
            - Use clear, technical language appropriate for developers
            
            Developer's question: {question}
            
            Please provide a helpful technical response:
            """
            
            result = qa_chain({"query": code_prompt})
            
            # Format response with sources
            response = result['result']
            
            if result.get('source_documents'):
                response += "\n\n**Documentation Sources:**\n"
                for i, doc in enumerate(result['source_documents'][:3]):
                    source = doc.metadata.get('source', 'Unknown')
                    response += f"- {Path(source).name}\n"
            
            return response
            
        except Exception as e:
            logger.error(f"Error in code helper: {str(e)}")
            return f"Error generating response: {str(e)}"

def create_gradio_interface(assistant: RAGAssistant):
    """Create Gradio interface for the RAG Assistant"""
    
    def upload_learning_files(files):
        if not files:
            return "No files uploaded."
        
        file_paths = [f.name for f in files]
        return assistant.load_documents(file_paths, "learning")
    
    def upload_code_files(files):
        if not files:
            return "No files uploaded."
        
        file_paths = [f.name for f in files]
        return assistant.load_documents(file_paths, "code")
    
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
    
    # Create Gradio interface
    with gr.Blocks(title="RAG-Based Learning & Code Assistant", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🎓 RAG-Based Learning & Code Assistant")
        gr.Markdown("Upload your documents and ask questions to get intelligent responses!")
        
        with gr.Tabs():
            # Learning Tutor Tab
            with gr.TabItem("📚 Learning Tutor"):
                gr.Markdown("### Personalized Learning Assistant")
                gr.Markdown("Upload textbooks, lecture notes, and study materials to get personalized learning assistance.")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        learning_files = gr.File(
                            label="Upload Learning Materials (PDF, TXT)",
                            file_count="multiple",
                            file_types=[".pdf", ".txt", ".md"]
                        )
                        learning_upload_btn = gr.Button("Upload Materials", variant="primary")
                        learning_status = gr.Textbox(label="Upload Status", interactive=False)
                    
                    with gr.Column(scale=2):
                        learning_chatbot = gr.Chatbot(
                            label="Learning Tutor Chat",
                            height=400
                        )
                        learning_input = gr.Textbox(
                            label="Ask a question about your course materials",
                            placeholder="e.g., Can you explain the concept of machine learning?"
                        )
                        learning_submit = gr.Button("Ask Question", variant="primary")
                
                learning_upload_btn.click(
                    upload_learning_files,
                    inputs=[learning_files],
                    outputs=[learning_status]
                )
                
                learning_submit.click(
                    learning_chat,
                    inputs=[learning_input, learning_chatbot],
                    outputs=[learning_chatbot, learning_input]
                )
                
                learning_input.submit(
                    learning_chat,
                    inputs=[learning_input, learning_chatbot],
                    outputs=[learning_chatbot, learning_input]
                )
            
            # Code Documentation Helper Tab
            with gr.TabItem("💻 Code Documentation Helper"):
                gr.Markdown("### Developer Documentation Assistant")
                gr.Markdown("Upload API documentation, code examples, and technical guides to get development assistance.")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        code_files = gr.File(
                            label="Upload Code Documentation (PDF, TXT, MD)",
                            file_count="multiple",
                            file_types=[".pdf", ".txt", ".md", ".py", ".js", ".json"]
                        )
                        code_upload_btn = gr.Button("Upload Documentation", variant="primary")
                        code_status = gr.Textbox(label="Upload Status", interactive=False)
                    
                    with gr.Column(scale=2):
                        code_chatbot = gr.Chatbot(
                            label="Code Helper Chat",
                            height=400
                        )
                        code_input = gr.Textbox(
                            label="Ask about APIs, code examples, or troubleshooting",
                            placeholder="e.g., How do I implement authentication in this API?"
                        )
                        code_submit = gr.Button("Ask Question", variant="primary")
                
                code_upload_btn.click(
                    upload_code_files,
                    inputs=[code_files],
                    outputs=[code_status]
                )
                
                code_submit.click(
                    code_chat,
                    inputs=[code_input, code_chatbot],
                    outputs=[code_chatbot, code_input]
                )
                
                code_input.submit(
                    code_chat,
                    inputs=[code_input, code_chatbot],
                    outputs=[code_chatbot, code_input]
                )
        
        # Footer
        gr.Markdown("---")
        gr.Markdown("*Powered by LangChain, ChromaDB, and Groq API*")
    
    return demo

def main():
    """Main function to run the application"""
    # Get Groq API key from environment variable
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if not groq_api_key:
        print("Please set your GROQ_API_KEY environment variable")
        print("You can get a free API key from: https://console.groq.com/")
        return
    
    try:
        # Initialize RAG Assistant
        print("Initializing RAG Assistant...")
        assistant = RAGAssistant(groq_api_key)
        
        # Create and launch Gradio interface
        demo = create_gradio_interface(assistant)
        
        print("Starting RAG-Based Learning & Code Assistant...")
        print("Access the application at: http://localhost:7860")
        
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            debug=True
        )
        
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()