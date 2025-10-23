from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv, find_dotenv
import os
from state.state_types import State


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 

def summarize_job_description(state: State):

    class LLMResponse(BaseModel):
        result_jd_summary: str
        result_job_title: str
        result_company_name: str

    parser = PydanticOutputParser(pydantic_object=LLMResponse)
    prompt_template = ChatPromptTemplate.from_template("""
    Here is the content we have from a job posting:
    {job_page_main_content}
    Your job is to summarize this content to what skills and qualities the job requires. Get rid off any information that would not be useful to a prospective applicant.
    Make sure to focus on the tools, skills, technologies required for this job especially keywords like the names of technologies and algorithms. Respond in plain text with no special characters and keep the answer to less than 200 words.
    The information you provide will be used to write a cover letter specific for this job. So be as descriptive as possible when it comes to the requirements.  
    In addition to this, use the information provided to identify the job position and the name of the company here.                                                                                             
    {format_instructions}""")
    
    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")

    result = (
        prompt_template | llm | parser
    ).invoke({
        "job_page_main_content": state["job_page_main_content"],
        "format_instructions": parser.get_format_instructions()
    })
    print('Summarized JD')
    return {
        "job_description_summary": result.result_jd_summary,
        "job_title": result.result_job_title,
        "company_name": result.result_company_name

    }
