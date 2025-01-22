import streamlit as st
from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, Settings, PromptTemplate
from llama_index.llms.openai import OpenAI  # We'll use OpenAI interface for LMStudio

from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Initialize the same models and settings as loader.py
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
Settings.embed_model = embed_model
llm = OpenAI(
    model="gpt-3.5-turbo",
    api_base="http://192.168.2.157:1234/v1",  # Default LMStudio port
    api_key="dummy",  # LMStudio doesn't need a real key
    temperature=0.7,
)
Settings.llm = llm


# Connect to Qdrant
client = QdrantClient(url="http://localhost", port=6333)
vector_store = QdrantVectorStore(client=client, collection_name="chat_with_notes")
index = VectorStoreIndex.from_vector_store(vector_store)
query_engine = index.as_query_engine(similarity_top_k=10)

# Streamlit UI
st.title("Chat with Your Notes")

# Create a text input box
query = st.text_input("Ask a question about your notes:")

# When the user enters a query
if query:
    with st.spinner("Searching..."):
        response = query_engine.query(query)
        qa_prompt_tmpl_str = (
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information above I want you to think step by step to answer the query in a crisp manner, incase case you don't know the answer say 'I don't know!'.\n"
            "Query: {query_str}\n"
            "Answer: "
            )

        qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)
        query_engine.update_prompts({"response_synthesizer:text_qa_template": qa_prompt_tmpl})
        response = query_engine.query(query)
        print(response)
        st.write("### Answer")
        st.write(response.response)
        
        # Optionally show source documents
        st.write("### Sources")
        for node in response.source_nodes:
            st.markdown(f"**Score:** {node.score:.4f}")
            st.markdown(f"**Content:** {node.node.text[:200]}...")
            st.markdown("---") 