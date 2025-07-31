
# 🤖 Multi-Agent Research Assistant  
**An AI-Powered Research and Report-Writing Application**

This project is a sophisticated multi-agent system built with **LangChain** that automates the end-to-end process of researching a given topic and generating a comprehensive, well-structured report. By orchestrating a team of specialized AI agents, the application efficiently handles complex tasks that would typically require manual effort.

The user provides a topic through a simple web interface, and the agents work together to deliver a final, polished Markdown report.

---

## 🚀 Key Features

- **Multi-Agent Architecture**  
  The system's core is a collaborative team of three distinct agents: a **Researcher**, a **Summarizer**, and a **Writer**. Each agent has a unique role, prompt, and a set of tools, allowing for a structured and reliable workflow.

- **Custom Tooling**  
  Agents are equipped with robust LangChain-compatible tools including:
  - `ddgs` for web searching,
  - a custom scraper (`scrape_website`),
  - file-saving functionality.

- **Google Gemini API Integration**  
  All agents use the **Google Gemini API** for advanced reasoning and text generation.

- **Interactive Web Interface**  
  Built with **Gradio**, the interface allows users to input a topic and view the final report in real-time.

---

## 🧠 Workflow & Data Flow

The application operates on a **sequential chain of command**, where the output of one agent becomes the input for the next. This ensures a logical and organized research process.

### 🕵️ Researcher Agent
- **Role**: Senior Research Analyst  
- **Goal**: Discover key trends and gather relevant sources.
- **Input**: User's topic  
- **Tools**:
  - `DuckDuckGoSearchRun`: To find relevant articles, blog posts, and data points.
  - `scrape_website`: To scrape content from found URLs.
- **Output**: Key findings, URLs, and scraped content.

### ✍️ Summarizer Agent
- **Role**: Professional Summarizer  
- **Goal**: Condense raw research into concise summaries.  
- **Input**: Researcher's findings  
- **Tools**: `DuckDuckGoSearchRun` (if clarification is needed)  
- **Output**: 2-3 paragraph summary highlighting major trends, players, and impacts.

### 🧾 Writer Agent
- **Role**: Senior Technology Report Writer  
- **Goal**: Compose a full-length, professional Markdown report.  
- **Input**: Summarized findings  
- **Tools**: None  
- **Output**: Final report saved as `research_report.md`

---

## 📈 Flow Diagram

```
[ User Input (Topic) ]  
        ↓  
[ Researcher Agent (Searches & Scrapes) ]  
        ↓  
[ Summarizer Agent (Condenses Research) ]  
        ↓  
[ Writer Agent (Composes Report) ]  
        ↓  
[ Final Report (Displayed in App & Saved to File) ]
```

---

## 🛠️ Getting Started

### ✅ Prerequisites

- Python **3.10+**
- Google API Key (for Gemini)

### 1. Environment Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate      # macOS/Linux
# venv\Scripts\activate       # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:  
`langchain`, `langchain-google-genai`, `ddgs`, `beautifulsoup4`, `gradio`, etc.

### 3. Configure Your API Key

Create a `.env` file in your project root:

```env
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
```

> ⚠️ Don’t forget to add `.env` to your `.gitignore` file.

### 4. Run the App

```bash
python app.py
```

Open the provided local URL (usually http://127.0.0.1:7860) in your browser.

---

## 📝 Project Files

| File | Description |
|------|-------------|
| `app.py` | Main script defining agents, tools, and logic |
| `requirements.txt` | All required dependencies |
| `research_report.md` | Auto-generated final report |
| `.env` | API key file (not included in repo) |

---

## 💡 How to Use

1. **Launch** the app:
   ```bash
   python app.py
   ```

2. **Enter a Topic**  
   Example: `"The impact of quantum computing on modern cryptography"`

3. **Click "Start Research"**  
   Triggers the full agentic workflow.

4. **Monitor Progress**  
   The terminal will display verbose steps from each agent.

5. **View Results**  
   The final report appears in the output box and is saved as `research_report.md`.

---

Made with ❤️ using LangChain, Gradio, and Gemini AI.
