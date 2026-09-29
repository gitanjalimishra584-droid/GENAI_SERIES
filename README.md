# 🤖 COGNIX — AI Agent

> An intelligent AI agent built with Python, LangChain, LangGraph, Groq and Streamlit.

COGNIX is a fast AI-powered conversational agent that can generate responses using an LLM, search Google when additional information is required, remember conversation context, and stream responses in real time.

## 🚀 Features

- ⚡ **Fast AI responses** powered by Groq
- 🔎 **Google Search integration** for information beyond the model's knowledge
- 🧠 **Conversation memory** using LangGraph MemorySaver
- 📡 **Real-time streaming responses**
- 🤖 **AI Agent architecture** using LangChain/LangGraph
- 💬 **Interactive chat interface** using Streamlit
- 🔐 Environment variables for API keys

## 🛠️ Tech Stack

- Python
- LangChain
- LangGraph
- Groq
- Streamlit
- Google Serper API
- dotenv

## 🧠 How COGNIX Works

1. User enters a question through the Streamlit interface.
2. The question is sent to the Groq-powered LLM.
3. The agent can decide to use Google Search when external information is needed.
4. Conversation state is maintained using LangGraph's `MemorySaver`.
5. The response is streamed to the user in real time.

## 📂 Project Structure

```text
GENAI_Series/
│
├── apps/
│   ├── cognix.py
│   ├── 1_qna_bot.py
│   └── 2_google_agent.py
│
├── notebooks/
│   ├── 1_basic_langchain.ipynb
│   ├── 2_prompts_chains.ipynb
│   ├── 3_basic_memory.ipynb
│   ├── 4_structured_output.ipynb
│   ├── 5_ollama_app.ipynb
│   ├── 6_groq_langchain.ipynb
│   ├── 7_streaming_responses.ipynb
│   ├── 8_basic_agent.ipynb
│   └── 9_google_search_agent.ipynb
│
├── requirements.txt
├── .gitignore
└── README.md

⚙️ Setup
Clone the repository:
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd GENAI_Series
Create and activate a virtual environment:
python -m venv env
source env/bin/activate
Install dependencies:
pip install -r requirements.txt
Create a .env file and add your API keys:
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
Run COGNIX:
streamlit run apps/cognix.py

⚡ Performance
COGNIX is designed for fast conversational interaction using Groq's inference infrastructure and streaming responses, allowing generated text to appear progressively instead of waiting for the complete response.

📚 Learning Journey
This project was built after learning core GenAI concepts including:
LangChain fundamentals
Prompting and chains
Memory
Structured outputs
Groq integration
Streaming
AI agents
Google Search tools
LangGraph

🔮 Future Improvements
Persistent database-backed memory
Better tool selection
Multiple conversation threads
Improved UI/UX
Additional tools
RAG integration
Deployment as a public web application