import streamlit as st
from pathlib import Path

from langchain_core.messages import AIMessage
from graph import workflow


st.title("JobPilot AI")
st.write("Your AI-powered job search assistant")


# --------------------------------------------------
# Optional Resume Upload
# --------------------------------------------------

resume = st.file_uploader(
    "Upload your resume (optional)",
    type=["pdf"]
)


# --------------------------------------------------
# User Query
# --------------------------------------------------

query = st.text_input(
    "Enter your job-related query:"
)


if st.button("Search"):

    if not query:
        st.warning("Please enter a query.")

    else:

        # --------------------------------------------------
        # Save resume ONLY if user uploaded one
        # --------------------------------------------------

        if resume:

            resume_path = Path(__file__).resolve().parent / "uploaded_resume.pdf"

            with open(resume_path, "wb") as f:
                f.write(resume.getbuffer())


        # --------------------------------------------------
        # Send ONLY the user's query to LangGraph
        # --------------------------------------------------

        user_query = query


        # --------------------------------------------------
        # Response placeholder
        # --------------------------------------------------

        response_placeholder = st.empty()

        final_response = ""


        # --------------------------------------------------
        # Stream LangGraph messages
        # --------------------------------------------------

        for message_chunk, metadata in workflow.stream(
            {
                "messages": [
                    ("user", user_query)
                ]
            },
            stream_mode="messages"
        ):

            # Only process AI messages
            if isinstance(message_chunk, AIMessage):

                # Ignore tool-call messages
                if message_chunk.tool_calls:
                    continue

                # Stream normal AI text
                if message_chunk.content:

                    final_response += message_chunk.content

                    response_placeholder.markdown(
                        final_response
                    )


        # --------------------------------------------------
        # No final response
        # --------------------------------------------------

        if not final_response:

            response_placeholder.warning(
                "No response was generated."
            )