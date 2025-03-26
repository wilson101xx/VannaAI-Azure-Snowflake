import streamlit as st
import requests
import pandas as pd

API_BASE_URL = "http://localhost:8000"

st.set_page_config(layout="wide")

# ---------------------- AUTH & INDEX CONFIG ----------------------
st.sidebar.title("Authentication")

# Index name for search
index_name = st.sidebar.text_input("Azure Search Index Name", value="test-vanna-index")


# ---------------------- NAVIGATION ----------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Query", "Training"])

# ---------------------- QUERY PAGE ----------------------
if page == "Query":
    st.title("Chatbot Query Interface")
    st.sidebar.title("Output Settings")
    show_sql = st.sidebar.checkbox("Show SQL", value=True)
    show_table = st.sidebar.checkbox("Show Table", value=True)
    show_summary = st.sidebar.checkbox("Show Summary", value=True)

    if st.sidebar.button("Show Suggested Questions"):
        response = requests.get(
            f"{API_BASE_URL}/query/suggested-questions",
            params={"index_name": index_name}
        )
        if response.status_code == 200:
            for question in response.json():
                if st.button(question):
                    st.session_state["my_question"] = question
        else:
            st.error("Error fetching suggested questions.")

    my_question = st.text_input("Ask a question about your data", st.session_state.get("my_question", ""))

    if st.button("Submit Query"):
        st.session_state["my_question"] = my_question
        st.write(f"**User:** {my_question}")
        response = requests.post(
            f"{API_BASE_URL}/query/ask",
            params={"index_name": index_name},
            json={"question": my_question}
        )
        if response.status_code == 200:
            result = response.json()
            if show_sql:
                st.write("### Generated SQL Query")
                st.code(result.get("gen_sql_qeury", "No SQL generated"), language="sql")
            if show_table and result.get("result_from_query"):
                st.write("### Query Results")
                st.dataframe(result["result_from_query"])
            if show_summary:
                st.write("### Summary")
                st.text(result.get("summary", "No summary available"))
        else:
            st.error(f"API Error: {response.json().get('detail', 'No detail provided')}")

# ---------------------- TRAINING PAGE ----------------------
elif page == "Training":
    st.title("Training Interface")

    training_endpoints = {
        "Train Info Schema": "/training/train_info_schema",
        "Train DDL": "/training/train_ddl"
    }

    for label, endpoint in training_endpoints.items():
        if st.button(label):
            response = requests.post(
                f"{API_BASE_URL}{endpoint}",
                params={"index_name": index_name}
            )
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

    document_text = st.text_area("Train on Business Documents")
    if st.button("Train Documents"):
        response = requests.post(
            f"{API_BASE_URL}/training/train_documents",
            params={"index_name": index_name},
            json={"document": document_text}
        )
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

    st.subheader("Train Prompt-SQL Pair")
    question = st.text_input("Prompt")
    sql = st.text_area("SQL")
    if st.button("Train Prompt/SQL Pair"):
        response = requests.post(
            f"{API_BASE_URL}/training/train_prompt_sql_pairs",
            params={"index_name": index_name},
            json={"question": question, "sql": sql}
        )
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

    if st.button("Get Training Data"):
        response = requests.get(
            f"{API_BASE_URL}/training/get_training_data",
            params={"index_name": index_name}
        )
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error("Failed to retrieve training data.")
