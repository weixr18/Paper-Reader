
def get_sys_prompt_summary(field_name):
    # summary prompt
    json_example = '{"short_summary": "XXX(concise summary)", "summary": "XXXXXX(detailed summary)"}'
    sys_prompt = f"""
    You are an expert in the field of **{field_name}**, and you will read a paper in this domain.  
    First, provide a **concise summary** of the paper’s contribution in **one sentence (in English)**, 
    such as *"A SOTA multi-threaded parallel SLAM system is proposed"*. It should be no more than **30 characters**.  
    Next, provide a **detailed summary** in **Chinese**, covering the **research background, problem addressed, main methods, and conclusions**. 
    This should meet the following criteria:  
    + **150-200 characters**  
    + **Clear and concise language**, emphasizing the key contributions of the paper  
    + **Not just based on the abstract**, but also considering the main content of the paper  
    + **Common academic terms such as SLAM and prompt should not be translated**  
    Finally, extract the information and format it as follows in **JSON**:  {json_example}  
    When responding, **only output the requested content** and **nothing else**.
    """
    return sys_prompt



def get_sys_prompt_extract(field_name):
    # extraction prompt
    json_example = '{"First Author": "Wenfeng Liang.", "Publication Year": "YYYY", "Research Objective": "XXXXXXX", "Sample Size": 150}'
    sys_prompt = f"""
    You are an expert in the field of {field_name}. You will read a paper in this field and extract the following information:
    + First Author: The full name of the first-ranked author.
    + Publication Year: The year of publication. If no year is provided, enter None.
    + Research Objective: A summary (10-30 words) of the main problem this research aims to solve.
    + Sample Size: The sample size used in the study. If not specified, enter None.

    Finally, output the extracted information in JSON format, for example: {json_example}
    When outputting, only provide the requested content and do not include any additional information.
    """
    return sys_prompt