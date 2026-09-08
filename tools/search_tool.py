from langchain_community.tools import DuckDuckGoSearchRun,tool

@tool
def search_tool(company):
    '''
    this tool is used to search the web for the details of company
    '''

    search=DuckDuckGoSearchRun()
    result=search.invoke(company)

    return {'company':company,'info':result}
