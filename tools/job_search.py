from langchain_community.tools import tool
from dotenv import load_dotenv
import os
import requests

load_dotenv()


@tool
def job_search(job_role, location):
    '''
    This tool uses Adzuna API to search for jobs online
    given the job role and location.
    '''

    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

    params = {
        "app_id": os.getenv("ADZUNA_APP_ID"),
        "app_key": os.getenv("ADZUNA_API_KEY"),
        "what": job_role,
        "where": location,
        "results_per_page": 5
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {
            "error": f"Adzuna API returned status {response.status_code}"
        }

    return response.json()