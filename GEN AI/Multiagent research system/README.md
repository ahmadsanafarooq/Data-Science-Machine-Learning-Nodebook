# 🤖 Multi-Agent Research Assistant
An AI-Powered Research and Report-Writing Application

This project is a sophisticated multi-agent system built with **LangChain** that automates the end-to-end process of researching a given topic and generating a comprehensive, well-structured report. By orchestrating a team of specialized AI agents, the application efficiently handles complex tasks that would typically require manual effort.

The user provides a topic through a simple web interface, and the agents work together to deliver a final, polished Markdown report.

---

## 🚀 Key Features

### Multi-Agent Architecture
The system's core is a collaborative team of three distinct agents: a **Researcher**, a **Summarizer**, and a **Writer**. Each agent has a unique role, prompt, and a set of tools, allowing for a structured and reliable workflow.

### Production-Ready Enhancements
The system is built for a production environment, featuring a robust testing suite, security guardrails, and graceful error handling to ensure reliability and safety.

### Custom Tooling
Agents are equipped with robust LangChain-compatible tools including:
- **ddgs** for web searching  
- **scrape_website** for scraping web content  
- **file-saving functionality**  

### Google Gemini API Integration
All agents use the **Google Gemini API** for advanced reasoning and text generation.

### Interactive Web Interface
Built with **Gradio**, the interface allows users to input a topic and view the final report in real-time.

---

## 🔒 Production-Readiness Enhancements

### Robust Testing Strategy
The project includes a comprehensive test suite using **pytest**:
- **Unit Tests**: Verify individual components in isolation.  
- **Integration Tests**: Confirm that different parts work together as expected.  
- **System Tests**: Perform an end-to-end workflow validation.  

### Safety & Security Guardrails
- **Input Validation**: Prevents off-topic or inappropriate requests.  
- **Output Validation**: Ensures correctness and relevance at every step.  
- **Resilient Retry Mechanism**: Retries failed tasks before stopping.  

### Deployment and Monitoring
- Easy deployment on **Hugging Face Spaces**.  
- `requirements.txt` handles dependencies.  
- Gradio interface is production-ready.  

---

## 🧠 Workflow & Data Flow

```
[ User Input (Topic) ]
        ↓
(Input Guardrail: Is the topic valid?)
        ↓
[ Researcher Agent (Searches & Scrapes) ]
        ↓
(Output Guardrail: Is the output valid? If not, retry.)
        ↓
[ Summarizer Agent (Condenses Research) ]
        ↓
(Output Guardrail: Is the output valid? If not, retry.)
        ↓
[ Writer Agent (Composes Report) ]
        ↓
(Output Guardrail: Is the output valid? If not, retry.)
        ↓
[ Final Report (Displayed in App & Saved to File) ]
```

---

## 🕵️ Agents

### Researcher Agent
- **Role**: Senior Research Analyst  
- **Goal**: Discover key trends and gather relevant sources.  
- **Tools**: DuckDuckGoSearchRun, scrape_website  
- **Output**: Key findings, URLs, scraped content  

### Summarizer Agent
- **Role**: Professional Summarizer  
- **Goal**: Condense raw research into summaries.  
- **Output**: 2–3 paragraph summary  

### Writer Agent
- **Role**: Senior Technology Report Writer  
- **Goal**: Compose a full-length Markdown report  
- **Output**: `research_report.md`  

---

## 🛠️ Getting Started

### ✅ Prerequisites
- Python 3.10+  
- Google API Key (for Gemini)  

### 1. Environment Setup
```bash
python3 -m venv venv
source venv/bin/activate      # macOS/Linux
# venv\Scripts\activate     # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Create a `.env` file in your project root:
```
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
```

⚠️ Add `.env` to `.gitignore`.

### 4. Run the App
```bash
python3 app.py
```
Open [http://127.0.0.1:7860](http://127.0.0.1:7860).

### 5. Run Tests
```bash
pytest
```

---

## 📝 Project Files

| File              | Description                                |
|-------------------|--------------------------------------------|
| `app.py`          | Main script defining agents, tools, logic |
| `requirements.txt`| All required dependencies                  |
| `research_report.md` | Auto-generated final report             |
| `README.md`       | Project documentation (this file)          |
| `tests/`          | Unit, integration, and system tests        |
| `.env`            | API key file         |

---

## 💡 How to Use

1. Launch the app:  
   ```bash
   python3 app.py
   ```

2. Enter a Topic  
   Example: *"The impact of quantum computing on modern cryptography"*  

3. Click **Start Research**  

4. Monitor Progress  
   Verbose logs from each agent appear in terminal.  

5. View Results  
   Final report appears in the UI and is saved as `research_report.md`.  

---

Made with ❤️ using **LangChain, Gradio, and Gemini AI**.
