from typing_extensions import TypedDict
from typing import Optional

class State(TypedDict, total=False):
    job_page_main_content: Optional[str]
    main_cover_letter: Optional[str]
    job_description_summary: Optional[str]
    final_cover_letter_content: Optional[str]
    job_title: Optional[str]
    company_name: Optional[str]
    job_url: Optional[str]
    updated_resume_yaml: Optional[str]
    experience_section: Optional[str]
    projects_section: Optional[str]
    publications_section: Optional[str]
    updated_experience: Optional[str]
    updated_projects: Optional[str]
    updated_publications: Optional[str]
    master_cv_path: Optional[str]
    updated_master_yaml_path: Optional[str]
    final_pdf_path: Optional[str]
    # Add more fields as needed for future outputs or node integration
