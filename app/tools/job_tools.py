from langchain_core.tools import tool
import requests



main_url="https://jsearch.p.rapidapi.com"
headers = {
        "x-rapidapi-key": "14fa3ea2ebmsh374056d9ee3878ep186035jsn7c25c8c7550f",
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
        "Content-Type": "application/json"
    }



# ----------JOB SEARCH----------
@tool
def get_job_search(query:str ,country:str, num_pages:str=1 , date_posted:str="all"):

    """
    Search for job listings.

    Args:
        query: Job title or keywords to search for.
        country: Country code where jobs should be searched (e.g. "ind", "us").
        num_pages: Number of result pages to retrieve.
        date_posted: Filter by posting date. One of:
            all
            today
            3days
            week
            month

    Returns:
        JSON response containing matching job listings.
    """

    url = f"{main_url}/search-v2"

    querystring = {"query":query,"num_pages":num_pages,"country":country,"date_posted":date_posted}

    print(f"---QUERY  STRING---{querystring}")

    response = requests.get(url, headers=headers, params=querystring)

    print(f"-----JOB SEARCH TOOL CALLED-----")

    print(response.json())
    return response.json()



# ----------JOB DETAILS BY JOB_ID----------
@tool
def get_details_of_job(job_id:str,country:str="us"):

    """
    Get Details of the job by using the job_id.

    Args:
        job_id: The ID of the job which the user wants to enquire.
        country: Country code where jobs should be searched (e.g. "ind", "us").

    Returns:
        JSON response containing the job details.
    """
    
    
    url = f"{main_url}/job-details"

    querystring = {"job_id":job_id,"country":country}

    print(f"---QUERY  STRING---{querystring}")

    response = requests.get(url, headers=headers, params=querystring)

    print(f"-----GET DETAILS OF JOB TOOL CALLED-----")
    return response.json()



# ----------JOB SALARY BY TITLE----------
@tool
def get_salary_job_by_title(job_title:str,location:str,location_type:str,years_of_experience:str="ALL"):

    """
    Get the salary details approximantion based on job title.

    Args:
        job_title: Job title for which to get salary estimation.

        location: Free-text location/area in which to get salary estimation.

        location_type: Specify the type of the location you are looking to get salary estimation for additional accuracy.Allowed values: 
                   ANY, CITY, STATE, COUNTRY

        years_of_experience: Get job estimation for a specific experience level range (years). Allowed values: 
                    ALL, LESS_THAN_ONE, ONE_TO_THREE, FOUR_TO_SIX, SEVEN_TO_NINE, TEN_TO_FOURTEEN, ABOVE_FIFTEEN

    Returns:
        JSON response containing matching job listings.
    """

    url = f"{main_url}/estimated-salary"

    print(f"---QUERY  STRING---{querystring}")

    querystring = {"job_title":job_title,"location":location,"location_type":location_type,"years_of_experience":years_of_experience}

    response = requests.get(url, headers=headers, params=querystring)

    print(f"-----SALARY BY JOB TOOL CALLED-----")
    return response.json()



# ----------JOB SALARY BY COMPANY----------
@tool
def get_salary_by_company(company:str ,job_title:str,location_type:str="ANY",years_of_experience:str="ALL"):

    """
    Get the salary details of a given company.

    Args:
        company: The company name for which to get salary information (e.g. Amazon).

        job_title: Job title for which to get salary estimation.

        location: Free-text location/area in which to get salary estimation.

        location_type: Specify the type of the location you are looking to get salary estimation for additional accuracy.Allowed values: 
                   ANY, CITY, STATE, COUNTRY

        years_of_experience: Get job estimation for a specific experience level range (years). Allowed values: 
                    ALL, LESS_THAN_ONE, ONE_TO_THREE, FOUR_TO_SIX, SEVEN_TO_NINE, TEN_TO_FOURTEEN, ABOVE_FIFTEEN

    Returns:
        JSON response containing matching job listings.
    """

    url = f"{main_url}/company-job-salary"

    querystring = {"company":company,"job_title":job_title,"location_type":location_type,"years_of_experience":years_of_experience}

    print(f"---QUERY  STRING---{querystring}")

    response = requests.get(url, headers=headers, params=querystring)

    print(f"-----SALARY BY COMPANY TOOL CALLED-----")
    return response.json()


job_tools=[get_job_search,get_details_of_job,get_salary_job_by_title,get_salary_by_company]
