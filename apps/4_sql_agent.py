from dotenv import load_dotenv
load_dotenv()

### db,llm,tools,create_agent,system_prompt,memory
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
import streamlit as st

db = SQLDatabase.from_uri("sqlite:///my_tasks.db")

db.run("""
       CREATE TABLE IF NOT EXISTS tasks (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       title TEXT NOT NULL,
       description TEXT,
       status TEXT CHECK(status IN('pending','in_progress','complete'))DEFAULT 'pending',
       created_at TIMESTAMP DEFAULT (datetime('now', '+5 hours', '+30 minutes'))
       );
 """)
print("DB Table Created Successfully ✅")

model= ChatGroq(model="openai/gpt-oss-20b",temperature=0)
toolkit= SQLDatabaseToolkit(db=db,llm=model)
tools = toolkit.get_tools()
# ------------------------- # System Prompt # ------------------------- 
system_prompt = """ 
You are a task management assistant connected to a SQLite database. The database contains a table named `tasks`.
 The `tasks` table has these columns: - id: INTEGER PRIMARY KEY - title: TEXT NOT NULL - description: TEXT - status: TEXT - created_at: TIMESTAMP Valid status values are ONLY: - pending - in_progress - complete 
IMPORTANT RULES: 1. Always inspect the database schema before writing SQL if you are unsure about the table structure.
 2. Use the SQL tools provided to you for all database operations.
 3. For SELECT queries, return at most 10 rows unless the user explicitly asks for fewer. 
 4. When listing tasks, order them by: created_at DESC 
 5. After INSERT, UPDATE, or DELETE operations, verify the change with a SELECT query.
  6. Never invent column names or table names. 
7. Never use a status value other than: pending, in_progress, complete 
 8. If the user asks to create a task and does not provide a status, use: pending 
9. If the user asks to list tasks, present the final results as a clean Markdown table. 
10. If the database operation fails, inspect the error, correct the SQL if possible, and try again. 
11. Do not claim that a database operation succeeded unless the database confirms it.
12. For normal conversational questions that do not require the database, answer normally. Your goal is to safely and accurately manage the user's tasks.
 """



@st.cache_resource
def get_agent():
    agent= create_agent(
    model= model,
    tools=tools,
    checkpointer=InMemorySaver(),
    system_prompt= system_prompt
    )
    return agent
agent= get_agent()

### Building Web Interface...
st.subheader(" 🗒️ TaskBot - Manage Your Tasks")
if "messages" not in st.session_state:
    st.session_state.messages= []
for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

    
prompt=st.chat_input("Ask me to manage your tasks..")
    

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("ai"):
        with st.spinner("Processing..."):
            response=agent.invoke(
                {"messages":[{"role":"user","content":prompt}]},
                {'configurable': {'thread_id': '1'}}
                )
            result= response["messages"][-1].content
            st.markdown(result)
            st.session_state.messages.append({"role":"ai","content":result})



