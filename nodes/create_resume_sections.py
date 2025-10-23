import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
import os                                                                                                                                                                                                          
from dotenv import load_dotenv
from state.state_types import State


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 

def create_resume_sections(state: State):
    class LLMResponse(BaseModel):
        updated_experience: str
        updated_projects: str
        updated_publications: str

    parser = PydanticOutputParser(pydantic_object=LLMResponse)

    prompt_template = ChatPromptTemplate.from_template("""
        Here is a summary of the requirements for a job I am applying to:
        {company_name} - {job_title}
        {job_description_summary}

        Here are ONLY the relevant sections of my resume in YAML format: experience, projects, publications:
        {experience}
        {projects}
        {publications}                                                                                    

        Your task is to update these sections to best target the job, following these instructions:
        - In experience, rephrase the highlights to best align with the job description if needed.
        - In projects, retain 2-3 of the most relevant projects and rephrase their highlights to best align with the job description if needed.
        - In publications, retain 1-3 of the most relevant publications and rephrase their highlights to best align with the job description if needed.
        - Do not hallucinate new experiences, projects, or publications, and do not introduce skills/technologies that are not in the original input.

        Return ONLY a single JSON object with this format:

        {{
            "updated_experience": "<updated experience section in YAML>",
            "updated_projects": "<updated projects section in YAML>",
            "updated_publications": "<updated publications section in YAML>"
        }}

        {format_instructions}
    """)

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.3-70b-versatile",
        temperature=0.5
    )

    result = (
        prompt_template | llm | parser
    ).invoke({
        "job_description_summary": state["job_description_summary"],
        "experience": state["experience_section"],
        "projects": state["projects_section"],
        "publications": state["publications_section"],
        "format_instructions": parser.get_format_instructions(),
        "company_name": state["company_name"],
        "job_title": state["job_title"]
    })
    print('Updated experience, projects, and publications from LLM')
    return {
        "updated_experience": result.updated_experience,
        "updated_projects": result.updated_projects,
        "updated_publications": result.updated_publications
    }
