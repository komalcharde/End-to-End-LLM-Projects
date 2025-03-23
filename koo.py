import os
import streamlit as st
import time
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

st.title("📄 Gemma Model Document Q&A")

# Function to create vector embeddings
def vector_embedding():
    if "vectors" not in st.session_state:
        # Load document embeddings
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        st.session_state.loader = PyPDFDirectoryLoader("./kk")  # Ensure the directory exists with PDFs
        st.session_state.docs = st.session_state.loader.load()
        
        # Check if documents are loaded
        if not st.session_state.docs:
            st.error("❌ No documents found in the directory './kk'. Please check and try again.")
            return

        st.write(f"✅ Loaded {len(st.session_state.docs)} documents.")  # Debugging statement
        
        # Split documents into smaller chunks
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
        
        # Check if document chunks are generated
        if not st.session_state.final_documents:
            st.error("❌ No document chunks generated. Please check the document content.")
            return

        st.write(f"✅ Split into {len(st.session_state.final_documents)} document chunks.")  # Debugging statement
        
        # Create FAISS vector store
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)
        st.success("✅ Vector Store is ready!")

# User input for document-based Q&A
user_query = st.text_input("💬 What do you want to ask from the document?")
if st.button("⚡ Create Vector Store"):
    vector_embedding()
    st.write("✅ Vector Store DB is ready!")

# Initialize the chat prompt template
prompt_template = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question.
    
    <context>
    <context>
    <context>
    
    Question: {input}
    """
)

# Processing user query
if user_query:
    # Ensure vector embeddings are created before running retrieval
    if "vectors" not in st.session_state:
        st.write("⚠️ Please create the Vector Store first by clicking 'Create Vector Store'.")
    else:
        # Initialize the Google Gemini AI model
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)

        # Retrieve relevant document chunks
        retriever = st.session_state.vectors.as_retriever()

        # Create the retrieval-based QA chain
        retrieval_chain = RetrievalQA.from_chain_type(
            llm=llm,  # ✅ Now using Google Gemini AI
            retriever=retriever,
            chain_type="map_reduce",
            return_source_documents=True
        )

        # Process the query
        start = time.process_time()
        response = retrieval_chain({"query": user_query})
        
        # Display the result
        st.subheader("💡 Answer:")
        st.write(response['result'])

        # Show source documents for reference
        with st.expander("📂 Document Similarity Search (Sources)"):
            for i, doc in enumerate(response.get("source_documents", [])):
                st.write(doc.page_content)
                st.write("📌 ---------------------------------------")
