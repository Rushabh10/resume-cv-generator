import os                                                                                                                                                                                                          
import yaml
from state.state_types import State

def get_cv_sections(state: State):
    file_path = "master_cv.yaml"
    with open(file_path, "r", encoding="utf-8") as file:
        yaml_content = yaml.safe_load(file)

    cv_content = yaml_content.get("cv", {})
    sections = cv_content.get("sections", {})

    return { "experience_section": sections.get("experience", []),
        "projects_section": sections.get("projects", []),
        "publications_section": sections.get("publications", []),
        "main_cover_letter": yaml_content.get("cv", "")}