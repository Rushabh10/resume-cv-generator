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


def create_cover_letter(state: State):
    class LLMResponse(BaseModel):
        result_cover_letter: str

    parser = PydanticOutputParser(pydantic_object=LLMResponse)
    prompt_template = ChatPromptTemplate.from_template("""
    Here is a summary of the requirements for a job I am applying to:
    {company_name} - {job_title}
    {job_description_summary}
    Here is a summary of my education, skills and experiences:   
    {main_cover_letter}   
    Your job is to write a cover letter based on my information that explains why I'm a great fit for the job. Use my education and experiences to craft a convincing story and highlight how my skills
    align with the job requirements and why I would be a good addition to the team. Do not hallucinate/create any new skills or experiences for me.  
    Add \n\n to split paragraphs where needed. The structure of the cover letter should be as follows:
    Introductory Paragraph with an overview of my education, skills and mentioning my current job.
    One paragraph on my work experiences and link how they are relevant to the job I am applying to.
    1-2 Paragraphs selecting relevant projects and publications which are related to the job I am applying to.
    1 paragraph about my soft-skills and extra curriculars and how they have played a role in developing other skills relevant to the job.
    A conclusion paragraph explaining why my combination of experiences and skills makes me an ideal candidate.   
    End my thanking the recruiter                                                                                                                                                                                                                                                                                                                                                                                                
    {format_instructions}""")
    
    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")

    result = (
        prompt_template | llm | parser
    ).invoke({
        "job_description_summary": state["job_description_summary"],
        "main_cover_letter": state['main_cover_letter'],
        "format_instructions": parser.get_format_instructions(),
        "company_name": state['company_name'],
        "job_title": state["job_title"]
    })
    print('Created Cover Letter')
    return {
        "final_cover_letter_content": result.result_cover_letter
    }
