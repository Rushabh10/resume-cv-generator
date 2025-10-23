from ruamel.yaml import YAML
import ast
from state.state_types import State


def replace_cv_sections(state: State):
    yaml = YAML()
    yaml.preserve_quotes = True

    master_yaml_path = "master_cv.yaml"
    updated_experience = state["updated_experience"]
    updated_projects = state["updated_projects"]
    updated_publications = state["updated_publications"]

    # Load the master YAML file
    with open(master_yaml_path, 'r', encoding='utf-8') as f:
        master_data = yaml.load(f)

    # Access the sections dict under cv
    sections = master_data.get('cv', {}).get('sections', {})

    def parse_section(section_str):
        if section_str:
            try:
                return ast.literal_eval(section_str)
            except Exception as e:
                print(f"Error parsing section string: {e}")
        return None

    # Parse and replace sections from state
    exp_obj = parse_section(updated_experience)
    if exp_obj is not None:
        sections['experience'] = exp_obj

    proj_obj = parse_section(updated_projects)
    if proj_obj is not None:
        sections['projects'] = proj_obj

    pub_obj = parse_section(updated_publications)
    if pub_obj is not None:
        sections['publications'] = pub_obj

    # Save updated YAML to new file
    company_name = state['company_name']
    filename = f"resume_{company_name}.yaml"
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(master_data, f)

    print("Replaced experience, projects, and publications in master YAML")

