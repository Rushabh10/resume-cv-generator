from state.state_types import State
from nodes.get_page_content import get_page_content
from nodes.summarize_job_description import summarize_job_description
from nodes.get_cv_sections import get_cv_sections
from nodes.create_cover_letter import create_cover_letter
from nodes.export_to_pdf import export_to_pdf
from nodes.create_resume_sections import create_resume_sections
from nodes.replace_cv_sections import replace_cv_sections
from nodes.create_rendercv_pdf import create_rendercv_pdf
from langgraph.graph import StateGraph, START, END

workflow = StateGraph(State)
workflow.add_node("get_page_content", get_page_content)
workflow.add_node("summarize_job_description", summarize_job_description)
workflow.add_node("get_cv_sections", get_cv_sections)
workflow.add_node("create_cover_letter", create_cover_letter)
workflow.add_node("export_to_pdf", export_to_pdf)
workflow.add_node("create_resume_sections", create_resume_sections)
workflow.add_node("replace_cv_sections", replace_cv_sections)
workflow.add_node("create_rendercv_pdf", create_rendercv_pdf)


workflow.add_edge(START, "get_page_content")
workflow.add_edge("get_page_content", "summarize_job_description")
workflow.add_edge("summarize_job_description", "get_cv_sections")
workflow.add_edge("get_cv_sections", "create_cover_letter")
workflow.add_edge("create_cover_letter", "export_to_pdf")
workflow.add_edge("export_to_pdf", "create_resume_sections")
workflow.add_edge("create_resume_sections", "replace_cv_sections")
workflow.add_edge("replace_cv_sections", "create_rendercv_pdf")
workflow.add_edge("create_rendercv_pdf", END)

if __name__ == "__main__":
    # Read job URLs from file
    with open("job_urls.txt", "r", encoding="utf-8") as f:
        job_urls = [line.strip() for line in f if line.strip()]

    chain = workflow.compile()  # Compile workflow once
    
    results = []
    for url in job_urls:
        input_state = State(job_url=url)  # Create typed State input per URL
        try:
            final_state = chain.invoke(input_state)  # Run workflow for this input
            results.append(final_state)
        except Exception as e:
            print(f"Error processing URL {url}: {e}")

    # Optionally, process or save results here
    print(f"Processed {len(results)} URLs successfully")
