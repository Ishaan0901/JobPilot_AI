# JobPilot AI

Your AI-powered job search assistant. Upload your resume, ask a question, and a tool-using LLM agent built with LangGraph searches live job listings, researches companies, and pulls context straight from your resume to answer you.

## Features

- **Resume-aware answers** — Upload a PDF resume; the agent retrieves relevant sections (skills, experience, education, projects) using a RAG pipeline to tailor its responses.
- **Live job search** — Looks up current job openings by role and location via the Adzuna Jobs API.
- **Company research** — Pulls up-to-date company information from the web via DuckDuckGo search.
- **Agentic tool routing** — A LangGraph state machine lets the LLM decide which tool(s) to call, chain multiple tool calls together, and reason over the results before responding.
- **Streamed responses** — Answers stream token-by-token into a Streamlit chat-style interface.

## How it works

1. You upload a resume (PDF) and type a query in the Streamlit app.
2. The resume path and query are passed into a LangGraph workflow.
3. A `chat_node` calls an LLM (Groq) that has three tools available:
   - `job_search` — queries the Adzuna API for job listings.
   - `resume_search` (RAG tool) — chunks and embeds your resume, then retrieves the most relevant passages for the query.
   - `company_search` — searches the web for company details.
4. If the LLM requests a tool, execution routes to a `tools` node, runs the tool, and loops back to `chat_node` so the LLM can reason over the result.
5. Once the LLM has enough information, it responds directly and the graph ends; the response streams live to the UI.

## Tech stack

| Layer | Technology |
|---|---|
| UI | [Streamlit](https://streamlit.io/) |
| Agent orchestration | [LangGraph](https://langchain-ai.github.io/langgraph/) |
| LLM | [Groq](https://groq.com/) (`openai/gpt-oss-20b`) via `langchain-groq` |
| Embeddings | `BAAI/bge-small-en-v1.5` via `langchain-huggingface` |
| Vector store | [Chroma](https://www.trychroma.com/) |
| PDF parsing | `pypdf` / `PyPDFLoader` |
| Job listings | [Adzuna API](https://developer.adzuna.com/) |
| Web search | `duckduckgo-search` |

## Project structure

```
JobPilot_AI/
├── app.py              # Streamlit front end
├── graph.py             # LangGraph state, nodes, and edges
├── llm.py                # LLM setup and tool binding
├── tools/
│   ├── job_search.py     # Adzuna job search tool
│   ├── RAG_Tool.py        # Resume retrieval (RAG) tool
│   └── search_tool.py     # Company web search tool
├── workflow.ipynb       # Notebook for visualizing the graph
└── requirements.txt
```

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Ishaan0901/JobPilot_AI.git
cd JobPilot_AI
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root with:

```
GROQ_API_KEY=your_groq_api_key
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_API_KEY=your_adzuna_api_key
```

- Get a Groq API key from [console.groq.com](https://console.groq.com/).
- Get Adzuna credentials from [developer.adzuna.com](https://developer.adzuna.com/).

### 4. Run the app

```bash
streamlit run app.py
```

Open the local URL Streamlit prints (usually `http://localhost:8501`), upload your resume, type a query, and hit **Search**.

## Example queries

- "Find remote Python developer jobs in Bangalore based on my resume."
- "What does my resume say about my machine learning experience?"
- "Tell me about Infosys and see if any of my listed skills match their open roles."

## Roadmap / known limitations

- The resume vector index is rebuilt on every query rather than cached, so repeated searches on the same resume are slower than necessary.
- Only PDF resumes are currently supported.
- No persistent chat history — each query is a fresh conversation.

## License

No license specified yet.
