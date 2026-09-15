# Tutorial 2: Consumer interfaces with a CKE in a Streamlit chatbot

## Introduction

In this tutorial, you’ll set up a custom retrieval augmented generation (RAG) pipeline to integrate knowledge from a Cortex Knowledge Extension into a chatbot.

This is how it works:

1. A Streamlit app accepts a prompt from a user.
2. The prompt is given to the Cortex Search Query API with the configured Cortex Knowledge Extension / Cortex Search Service.
3. The Streamlit app takes the retrieved documents, puts them into the context window with a custom prompt, and sends it to the Cortex LLM Complete function with a specified LLM.

Note

This tutorial assumes that you have a CKE already available. Go to the [Snowflake Marketplace](https://app.snowflake.com/_deeplink/marketplace) and access one, or use [Tutorial 1](/user-guide/snowflake-cortex/cortex-knowledge-extensions/tutorials/setup-test-cke-tutorial) to create one.

![A flowchart showing the CKE workflow, from a provider's cortex search service, to a search index, to a response in a consumer's prompt.](/static/images/cortex-knowledge-extensions/cke-workflow-complete.png)

# Step 1. Set up your environment

The example below sets up an environment and creates a Streamlit application that you can run in Snowflake to test out a Cortex Knowledge Extension. This assumes the Consumer has access to a Cortex Knowledge Extension that’s been shared by a Provider.

1. sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. in the navigation menu, select **Projects** » **Streamlit**.
3. Select **+ Streamlit App**.

   The **Create Streamlit App** window opens.
4. Enter a name for your app.
5. In the **App location** dropdown, select the database and schema for your app.
6. In the **Warehouse** dropdown, select the warehouse where you want to run your app and execute queries.
7. Select **Create**.

   > The Streamlit in Snowflake editor opens an example Streamlit app in Viewer mode. Viewer mode allows you to see how the Streamlit application appears to users.
8. Verify that the correct packages and versions are installed as in the image below.

![A screenshot showing the packages required to be installed in order to use CKE.](/static/images/cortex-knowledge-extensions/cke-required-packages.png)

## Step 2: Create a Streamlit app for your CKE chat tester

The code below is a simple Streamlit app that allows you to test the CKE. The app uses the Snowflake ML Python package to call the Cortex Knowledge Extension and the Snowflake LLM Complete function.
The app allows you to select a Cortex Knowledge Extension, enter a question, and receive a response from the LLM. The app also provides options for debugging and using chat history.

1. In the navigation menu, select **Projects** » **Streamlit**.
2. Select the Streamlit app you created in the previous step.
3. In the Streamlit in Snowflake editor, select **Edit** » **Edit code**.
   The Streamlit in Snowflake editor opens in Edit mode.
4. In the left navigation bar, select **streamlit\_app.py** to open the code editor.
5. In the code editor, delete the existing code.
6. Copy the code below and paste it into the code editor, then select **Save** » **Save and run**.
   The Streamlit in Snowflake editor runs the app and opens it in Viewer mode.

Copy code

```
import streamlit as st
from snowflake.core import Root
from snowflake.cortex import Complete
from snowflake.snowpark.context import get_active_session

MODELS = [
    "llama3.1-8b",
    "llama3.1-70b",
    "llama3.1-405b"
]

def init_messages():
    """Initialize session state messages if not present or if we need to clear."""
    if st.session_state.get("clear_conversation") or "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.clear_conversation = False

def init_service_metadata():
    """Load or refresh cortex search services from Snowflake."""
    services = session.sql("SHOW CORTEX SEARCH SERVICES IN ACCOUNT;").collect()
    service_metadata = []
    if services:
        for s in services:
            svc_name = s["name"]
            svc_schema = s["schema_name"]
            svc_db = s["database_name"]
            svc_search_col = session.sql(
                f"DESC CORTEX SEARCH SERVICE {svc_db}.{svc_schema}.{svc_name};"
            ).collect()[0]["search_column"]
            service_metadata.append(
                {
                    "name": svc_name,
                    "search_column": svc_search_col,
                    "db": svc_db,
                    "schema": svc_schema,
                }
            )

    st.session_state.service_metadata = service_metadata

    # Initialize selected_cortex_search_service if it doesn't exist
    if "selected_cortex_search_service" not in st.session_state and service_metadata:
        st.session_state.selected_cortex_search_service = service_metadata[0]["name"]

    selected_entry = st.session_state.get("selected_cortex_search_service")

    if selected_entry:
        # Find matching service metadata
        selected_service_metadata = next(
            (svc for svc in st.session_state.service_metadata if svc["name"] == selected_entry),
            None
        )

        if selected_service_metadata:
            # Store them in session_state
            st.session_state.selected_schema = selected_service_metadata["schema"]
            st.session_state.selected_db = selected_service_metadata["db"]
        elif st.session_state.get("debug", False):
            st.write("No matching service found for:", selected_entry)

def init_config_options():
    if "service_metadata" not in st.session_state or not st.session_state.service_metadata:
        st.sidebar.warning("No Cortex Knowledge Extensions available")
        return

    st.sidebar.selectbox(
        "Select Cortex Knowledge Extension",
        [s["name"] for s in st.session_state.service_metadata],
        key="selected_cortex_search_service",
    )
    if st.sidebar.button("Clear conversation"):
        st.session_state.clear_conversation = True

    # If st.sidebar.toggle isn't available, use st.sidebar.checkbox:
    st.sidebar.checkbox("Debug", key="debug", value=False)
    st.sidebar.checkbox("Use chat history", key="use_chat_history", value=True)

    with st.sidebar.expander("Advanced options"):
        st.selectbox("Select model:", MODELS, key="model_name")
        st.number_input(
            "Select number of context chunks",
            value=5,
            key="num_retrieved_chunks",
            min_value=1,
            max_value=10,
        )
        st.number_input(
            "Select number of messages to use in chat history",
            value=5,
            key="num_chat_messages",
            min_value=1,
            max_value=10,
        )

    st.sidebar.expander("Session State").write(st.session_state)

def get_chat_history():
    """Get the last N messages from session state."""
    start_index = max(
        0, len(st.session_state.messages) - st.session_state.num_chat_messages
    )
    return st.session_state.messages[start_index : len(st.session_state.messages) - 1]

def complete(model, prompt):
    """Use the chosen Snowflake cortex model to complete a prompt."""
    return Complete(model=model, prompt=prompt).replace("$", "\\$")

def make_chat_history_summary(chat_history, question):
    """
    Summarize the chat history plus the question using your LLM,
    to refine the final search query.
    """
    prompt = f"""
    [INST]
    Based on the chat history below and the question, generate a query that extend the question
    with the chat history provided. The query should be in natural language.
    Answer with only the query. Do not add any explanation.

    <chat_history>
    {chat_history}
    </chat_history>
    <question>
    {question}
    </question>
    [/INST]
    """
    summary = complete(st.session_state.model_name, prompt)
    if st.session_state.debug:
        st.sidebar.text_area("Chat history summary", summary.replace("$", "\\$"), height=150)
    return summary

def query_cortex_search_service(query, columns=[], filter={}):
    """
    Query the selected cortex search service with the given query and retrieve context documents.
    """
    # Safely retrieve from session_state
    db = st.session_state.get("selected_db")
    schema = st.session_state.get("selected_schema")

    if st.session_state.get("debug", False):
        st.sidebar.write("Query:", query)
        st.sidebar.write("DB:", db)
        st.sidebar.write("Schema:", schema)
        st.sidebar.write("Service:", st.session_state.selected_cortex_search_service)

    cortex_search_service = (
        root.databases[db]
        .schemas[schema]
        .cortex_search_services[st.session_state.selected_cortex_search_service]
    )

    context_documents = cortex_search_service.search(
        query,
        columns=columns,
        filter=filter,
        limit=st.session_state.num_retrieved_chunks
    )

    results = context_documents.results

    if st.session_state.get("debug", False):
        st.sidebar.write("Search Results:", results)

    service_metadata = st.session_state.service_metadata
    search_col = [
        s["search_column"] for s in service_metadata
        if s["name"] == st.session_state.selected_cortex_search_service
    ][0].lower()

    # Build a context string for the prompt
    context_str = ""
    context_str_template = (
        "Source: {source_url}\n"
        "Source ID: {id}\n"
        "Excerpt: {chunk}\n\n\n"
    )
    for i, r in enumerate(results):
        context_str += context_str_template.format(
            id=i+1,
            chunk=r[search_col],
            source_url=r["source_url"],
            title=r["document_title"],
        )
    if st.session_state.debug:
        st.sidebar.text_area("Context documents", context_str, height=500)

    return context_str, results

def create_prompt(user_question):
    """
    Combine user question, context from the search service, and chat history
    to create a final prompt for the LLM.
    """
    if st.session_state.use_chat_history:
        chat_history = get_chat_history()
        if chat_history != []:
            question_summary = make_chat_history_summary(chat_history, user_question)
            prompt_context, results = query_cortex_search_service(
                question_summary, columns=["chunk", "source_url", "document_title"]
            )
        else:
            prompt_context, results = query_cortex_search_service(
                user_question, columns=["chunk", "source_url", "document_title"]
            )
    else:
        prompt_context, results = query_cortex_search_service(
            user_question, columns=["chunk", "source_url", "document_title"]
        )
        chat_history = ""

    prompt = f"""
You are a helpful AI assistant with RAG capabilities. When a user asks you a question, you will also be given excerpts from relevant documentation to help answer the question accurately. Please use the context provided and cite your sources using the citation format provided.

Context from documentation:
{prompt_context}

User question:
{user_question}

OUTPUT:
"""

    # Add prompt to debug window
    if st.session_state.get("debug", False):
        st.sidebar.text_area("Complete Prompt", prompt, height=300)

    return prompt, results

def post_process_citations(generated_response, results):
    """
    Replace {{.StartCitation}}X{{.EndCitation}} with bracketed references to actual product links.

    NOTE: If the model references chunks out of range (like 4 if only 2 exist),
    consider adding logic to remap or drop invalid references.
    """
    used_results = set()
    for i, ref in enumerate(results):
        old_str = f"{{.StartCitation}}{i+1}{{.EndCitation}}"
        replacement = f"[{i+1}]{ref['source_url']})"
        new_resp = generated_response.replace(old_str, replacement)
        if new_resp != generated_response:
            used_results.add(i)
        generated_response = new_resp
    return generated_response, used_results

# ------------------------------------------------------------------------------
# (2) Main Application (with improved UI)
# ------------------------------------------------------------------------------

def main():
    # Optional: wide layout, custom page title
    st.set_page_config(
        page_title="Cortex Knowledge Extension Chat Tester",
        layout="wide",
    )

    # Optional: a bit of custom CSS for bubble spacing
    custom_css = """
    <style>
    [data-testid="stChatMessage"] {
        border-radius: 8px;
        margin-bottom: 1rem;
        padding: 10px;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # Title or subheader for your app
    st.subheader("Cortex Knowledge Extension Chat Tester")

    # Initialize metadata and config
    init_service_metadata()
    init_config_options()
    init_messages()

    # Icons for user/assistant
    icons = {"assistant": "❄️", "user": "👤"}

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=icons[message["role"]]):
            st.markdown(message["content"])

    # If there are no services, disable chat
    disable_chat = (
        "service_metadata" not in st.session_state
        or len(st.session_state.service_metadata) == 0
    )

    # Chat input
    if question := st.chat_input("Ask a question...", disabled=disable_chat):
        # 1. Store user message
        st.session_state.messages.append({"role": "user", "content": question})

        # 2. Display user bubble
        with st.chat_message("user", avatar=icons["user"]):
            st.markdown(question.replace("$", "\\$"))

        # 3. Prepare assistant response
        with st.chat_message("assistant", avatar=icons["assistant"]):
            message_placeholder = st.empty()

            # Clean the question
            question_safe = question.replace("'", "")

            # Build prompt and retrieve docs
            prompt, results = create_prompt(question_safe)

            with st.spinner("Thinking..."):
                generated_response = complete(st.session_state.model_name, prompt)

                # Post-process citations
                post_processed_response, used_results = post_process_citations(generated_response, results)

                # Build references table (only if there are results)
                if results:
                    markdown_table = "\n\n###### References \n\n| Index | Title | Source |\n|------|-------|--------|\n"
                    for i, ref in enumerate(results):
                        # Include all references that were found
                        markdown_table += (
                            f"| {i+1} | {ref.get('document_title', 'N/A')} | "
                            f"{ref.get('source_url', 'N/A')} |\n"
                        )
                else:
                    markdown_table = "\n\n*No references found*"

                # Show final assistant message (with references)
                message_placeholder.markdown(post_processed_response + markdown_table)

        # 4. Append final assistant message to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": post_processed_response + markdown_table}
        )

# ------------------------------------------------------------------------------
# (3) Entry Point
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    session = get_active_session()
    root = Root(session)
    main()
```

## Step 3: Test the app

1. Click **Run** to launch the Streamlit application.
2. Select a CKE from the drop down menu on the left pane under **Select Cortex Knowledge Extension**.`
3. Ask a question in the chat text box.

![A screenshot showing the "Ask a question" chat text box.](/static/images/cortex-knowledge-extensions/cke-chat-tester.png)
