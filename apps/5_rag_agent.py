from dotenv import load_dotenv
load_dotenv()


from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import InMemoryVectorStore
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st


### data in st session

if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded = False

if "agent" not in st.session_state:
    st.session_state.agent = None

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "messages" not in st.session_state:
    st.session_state.messages = []
    


def process_document(path):

    ## load the documents
    loader = PyPDFDirectoryLoader(path)
    docs = loader.load()

    ## split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    docs = splitter.split_documents(documents=docs)


    ## embeddings and Vector DB
    embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)
    vector_db = InMemoryVectorStore.from_documents(
        documents=docs,
        embedding=embeddings
    )


    ## create a agent - tool, llm, prompt
    llm = ChatGroq(model="openai/gpt-oss-20b")

    @tool
    def retrieve_context(query:str):
        """Retrieve documents relevant to a query from the knowledge base."""
        context = ""
        docs = vector_db.similarity_search(query=query, k=8)
        for doc in docs:
            context = doc.page_content + "\n\n"

        return context 


    system_prompt = """You are a helpful assistant that answers questions
using the uploaded document.

Always use the retrieve_context tool to find relevant information
before answering questions about the uploaded document.

Answer directly using the retrieved text. Pay close attention to
numeric values, test names, units, dates, and reference ranges.

Do not claim that information is missing if it appears in the
retrieved text. If the answer is not present in the retrieved text,
clearly say that you could not find it.

Do not invent values or facts. For medical reports, explain what
the report states without making a diagnosis."""


    memory = InMemorySaver()

    agent = create_agent(
        model=llm,
        tools=[retrieve_context],
        system_prompt=system_prompt,
        checkpointer=memory
    )

    st.session_state.agent = agent
    st.session_state.document_uploaded = True



### upload ui
if not st.session_state.document_uploaded:
    uploaded = st.file_uploader(label="Select PDF Files", type=["pdf"], accept_multiple_files=True)
    if uploaded:
        with st.spinner("Processing..."):
            path = "./doc_files/"
            for file in uploaded:
                with open(path + file.name, "wb") as f:
                    f.write(file.getvalue())

            process_document(path)
            st.rerun()

            
## chat ui

if st.session_state.document_uploaded and st.session_state.agent:
    for message in st.session_state.messages:
        role = message.get("role")
        content = message.get("content")
        st.chat_message(role).markdown(content)


    query = st.chat_input("Ask anything related to uploaded documents....")
    if query:
        st.session_state.messages.append({"role":"user", "content":query})

        st.chat_message("user").markdown(query)
        response = st.session_state.agent.invoke(
            {"messages":[{"role":"user", "content":query}]},
            {"configurable":{"thread_id":1}}
        )

        answer = response["messages"][-1].content
        st.chat_message("ai").markdown(answer)
        st.session_state.messages.append({"role":"ai", "content":answer})