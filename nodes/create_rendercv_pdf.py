import subprocess
import shutil
import os
import sys
from state.state_types import State

def create_rendercv_pdf(state: State):
    company_name = state["company_name"]
    filename = f"resume_{company_name}.yaml"
    pdf_filename = filename.replace('.yaml', '.pdf')
    current_dir = os.getcwd()
    rendercv_output_dir = os.path.join(current_dir, "rendercv_output")
    
    # Build command to activate conda env and run rendercv
    # Use shell=True with combined command (Linux/Mac example)
    # Adjust activation command for Windows if needed
    conda_activate_cmd = "conda activate llm_env"
    rendercv_cmd = f'rendercv render "{filename}"'
    
    full_cmd = f'bash -c {conda_activate_cmd} && {rendercv_cmd}'

    # print(full_cmd)
    
    try:
        # Run the command in shell with activated env
        subprocess.run(full_cmd, shell=True, check=True, executable='/bin/bash')
        
        # Expect PDF output inside rendercv_output folder
        pdf_source_path = None
        # Find the pdf file in rendercv_output folder
        for entry in os.listdir(rendercv_output_dir):
            if entry.lower().endswith('.pdf'):
                pdf_source_path = os.path.join(rendercv_output_dir, entry)
                break
        if pdf_source_path is None:
            raise FileNotFoundError("No PDF file found in rendercv_output folder after rendercv run")
        
        # Destination PDF path in current directory
        pdf_dest_path = os.path.join(current_dir, pdf_filename)
        
        # Move and rename the PDF to current directory
        shutil.move(pdf_source_path, pdf_dest_path)
        
        # Delete the rendercv_output folder and its contents
        shutil.rmtree(rendercv_output_dir)
        
        print(f"PDF generated and moved to {pdf_dest_path}")
        return {"final_pdf_path": pdf_dest_path}
    
    except subprocess.CalledProcessError as e:
        print("Error running rendercv command:", e, file=sys.stderr)
        return {"error": str(e)}
    except Exception as e:
        print("Unexpected error:", e, file=sys.stderr)
        return {"error": str(e)}
