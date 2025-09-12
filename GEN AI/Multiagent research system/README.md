
# Multi-Agent Research Assistant

## Overview
This project implements a **production-ready multi-agent system** designed for automated research.  
It uses modular agents for researching, summarizing, and writing content, orchestrated via a workflow.  
The system includes **Gradio-based UI**, testing, logging, error handling, and secrets management.

---

## Features
- 🔍 **Researcher Agent** → Gathers information from knowledge sources.  
- ✍️ **Summarizer Agent** → Condenses research findings.  
- 📄 **Writer Agent** → Produces final structured reports.  
- 🧩 **Workflow Orchestration** → Seamless agent-to-agent collaboration.  
- 🧪 **Comprehensive Testing** → Unit, integration, and system-level tests.  
- 🛡 **Safety & Resilience** → Error handling, logging, and monitoring.  
- 🎨 **User Interface** → Gradio app for accessibility.  
- 🔐 **Secrets Management** → `.env` file ensures API keys and configs remain secure.  

---

## Repository Structure
```
src/
├── agents/
│   ├── researcher.py
│   ├── summarizer.py
│   └── writer.py
│
├── utils/
│   ├── logging_utils.py
│   └── exceptions.py
│
├── workflows/
│   └── research_workflow.py
│
├── main.py
│
tests/
├── test_unit.py
├── test_integration.py
└── test_system.py
│
.env
.gitignore
LICENSE
README.md
requirements.txt
research_report.md
```

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/multi-agent-research-assistant.git
   cd multi-agent-research-assistant
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file to securely store your API keys and configs.

---

## Usage
Run the Gradio UI with:
```bash
python src/main.py
```

This launches a web-based interface to interact with the Research Assistant.

---

## Testing
- Unit tests: `pytest tests/test_unit.py`  
- Integration tests: `pytest tests/test_integration.py`  
- System tests: `pytest tests/test_system.py`  

---

## Safety & Resilience
- ✅ Centralized logging for monitoring and debugging.  
- ✅ Custom exceptions for robust error handling.  
- ✅ Modular design for scalability and maintainability.  
- ✅ Troubleshooting guide included in documentation.  

---

## Documentation
- **README.md** → Project overview & usage.  
- **research_report.md** → Example generated report.  
- **LICENSE** → Open-source compliance.  

---

## Contribution Guidelines
1. Fork the repo and create a new branch.  
2. Make your changes and add tests.  
3. Submit a pull request for review.  

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements
- Built as part of **Agentic AI** coursework.  
- Inspired by advances in LLM-powered agent workflows.  
