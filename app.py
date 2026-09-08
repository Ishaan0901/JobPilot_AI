import streamlit as st
import tempfile

from langchain_core.messages import AIMessage
from graph import workflow


st.title("JobPilot AI")
st.write("Your AI-powered job search assistant")


# Resume upload
resume = st.file_uploader(
    "Upload your resume",
    type=["pdf"]
)


# User query
query = st.text_input(
    "Enter your job-related query:"
)


if st.button("Search"):

    if not query:
        st.warning("Please enter a query.")

    elif not resume:
        st.warning("Please upload your resume.")

    else:

        # Save resume temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(resume.getbuffer())
            resume_path = temp_file.name.replace("\\", "/")


        # Send resume path + query to agent
        user_query = f"""
Resume path: {resume_path}

User query:
{query}
"""


        # Response placeholder
        response_placeholder = st.empty()

        final_response = ""


        # Stream LangGraph messages
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

                # Ignore AI tool-call messages
                if message_chunk.tool_calls:
                    continue

                # Stream normal AI text
                if message_chunk.content:

                    final_response += message_chunk.content

                    response_placeholder.markdown(
                        final_response
                    )


        # No final response
        if not final_response:

            response_placeholder.warning(
                "No response was generated."
            )
