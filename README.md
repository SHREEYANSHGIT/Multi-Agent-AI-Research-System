# Multi-Agent AI Research System (ResearchMind)

**Developed by Shreeyansh Asati**  
**An AI/ML Engineer**

DEMO : https://multi-agent-ai-research-system-by-shreeyansh.streamlit.app/ <br>
LINKEDIN : https://www.linkedin.com/in/shreeyansh-asati-18shreey/<br>
GITHUB : https://github.com/SHREEYANSHGIT/<br>

ResearchMind is an advanced multi-agent AI research pipeline that autonomously gathers, reads, writes, and evaluates research reports on any given topic. Built with LangGraph, LangChain, Groq, and Streamlit, this system divides cognitive tasks into distinct agents to produce comprehensive, high-quality, and peer-reviewed research outputs.

## 🌟 Key Features

- **Multi-Agent Architecture:** Four highly specialized agents working seamlessly in a pipeline:
  1. **🔍 Search Agent:** Gathers recent, reliable web information using the Tavily API.
  2. **📄 Reader Agent:** Scrapes and extracts deep content from top web sources.
  3. **✍️ Writer Chain:** Synthesizes the gathered data into a structured research report (Introduction, Key Findings, Conclusion, Sources).
  4. **🧐 Critic Chain:** Acts as a strict peer reviewer, evaluating the report for strengths, areas to improve, and assigning a score.
- **Dynamic Model Selection:** Easily switch between state-of-the-art open-source models directly from the UI (`llama-3.1-8b-instant`, `qwen/qwen3-32b`, `llama-3.3-70b-versatile`). Includes built-in fallbacks to ensure uninterrupted execution.
- **Stunning Streamlit Interface:** Features a modern, neon-infused UI with live progress indicators and expanding result panels.
- **CLI Support:** Run the pipeline interactively through the terminal using `pipeline.py`.
- **Lightning Fast Inference:** Powered by Groq's LPU inference engine for near-instantaneous LLM responses.

## 🛠️ Technology Stack

- **Frameworks:** LangChain, LangGraph, Streamlit
- **LLM Provider:** Groq (Llama 3, Qwen)
- **Web Search & Scraping:** Tavily Search API, BeautifulSoup4, Requests
- **Environment Management:** Python `dotenv`

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.10+ installed.

### Installation

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd Multi-Agent-AI-Research-System
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install streamlit
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add your API keys:
   ```env
   GROQ_API_KEY="your_groq_api_key"
   TAVILY_API_KEY="your_tavily_api_key"
   ```

## 🎮 Usage

### 1. Web Interface (Streamlit)
To launch the beautiful graphical user interface, run:
```bash
python -m streamlit run Main_agent/app.py
```
- Enter your research topic.
- Select your preferred language model from the dropdown.
- Watch the agents work in real-time and download your final markdown report!

### 2. Command Line Interface (CLI)
If you prefer the terminal, you can run the pipeline directly:
```bash
python Main_agent/pipeline.py
```
Follow the prompt to enter your research topic.

## 🏗️ Project Structure

- `Main_agent/app.py`: The Streamlit web interface.
- `Main_agent/pipeline.py`: The core execution logic connecting the agents.
- `Main_agent/agents.py`: Defines the search/reader agents and the writer/critic chains alongside model selection logic.
- `Main_agent/tools.py`: Contains the web search and scraping tool functions.
- `requirements.txt`: Project dependencies.
