from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END , START
from llm import llm_with_tools,tools
from langgraph.prebuilt import ToolNode,tools_condition


#   State
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]



#   Tool Node
tool_node=ToolNode(tools)


#   Chat Node:
from langchain_core.messages import BaseMessage, SystemMessage


def chat_node(state):
    '''
    This is the chat node which is used to chat with the llm
    '''

    system_message = SystemMessage(content="""
    You are an AI Job Assistant.

    You have access to three tools:

    1. job_search
       - Use this when the user wants to search for jobs.
       - Use the user's job role and location when available.

    2. resume_search
       - Use this when you need information from the user's resume.
       - Use it to evaluate the user's skills, experience, projects, education, etc.

    3. company_search
       - Use this when you need information about a company.
       - Use it to research company details, background, products, or other relevant information.

    Tool usage:
    - Decide yourself which tool is needed based on the user's request.
    - Use multiple tools when necessary.
    - After receiving a tool result, reason about the result before deciding what to do next.
    - Do not make up information that could be obtained from a tool.

    When displaying job results in a Markdown table:
    - Keep the same number of columns in every row.
    - Never use the | character inside a table cell.
    - Do not create empty columns.
    - If information is missing, write "Not specified".
    """)

    result = llm_with_tools.invoke(
        [system_message] + state['messages']
    )

    return {'messages': [result]}



#   Graph
graph=StateGraph(State)

#   Add Nodes:
graph.add_node('chat_node',chat_node)
graph.add_node('tools',tool_node)

#   Add Edges:
graph.add_edge(START,'chat_node')
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")



#   Compile the graph:
workflow=graph.compile()

