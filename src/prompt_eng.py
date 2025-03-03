import json
def get_sys_prompt_summary(field_name):
    # summary prompt
    output_example = json.dumps({
    "short_summary": "Proposes a xxx system for xxx",
    "long_summary": {
        "research_context": "The field of xxx faces challenges such as...",
        "problem_statement": "Existing methods fail to address...",
        "methodology": "By combining xxx with xxx...",
        "conclusions": "Experiments demonstrate that..."
    }})
    sys_prompt = f"""
    You are a top expert in the field of {field_name}, tasked with analyzing an English research paper in this domain. Please follow these steps:
    1. **Short Summary**: Provide a one-sentence summary of the paper's core contribution in English. Requirements:
      - Focus on methodological innovation (e.g., "Proposes a real-time SLAM system integrating Transformer")
      - Include technical keywords (e.g., multi-threaded, lightweight, end-to-end)
      - Strictly limit to 30 words or fewer
    2. **Long Summary**: Provide a structured summary in English (150-200 words) covering the following:
      - Research Context: Identify the key challenges or gaps in the field that the paper addresses.
      - Problem Statement: Clearly state the specific problem the paper tackles.
      - Methodology: Highlight the innovative technical approach (keep domain-specific terms like SLAM in their original form).
      - Conclusions: Summarize the experimental results and practical implications.
    Note: Ensure the summary is based on a thorough reading of the main text, especially the Method and Experiment sections.
    3. **Format Output**: Generate a JSON output strictly following this format:
    {output_example}
    4. *Do not include any additional comments or explanations in the output.*
    """
    return sys_prompt



def get_sys_prompt_extract(field_name):
    # extraction prompt
    output_example = {
    "first_author": "Michael J. Black",
    "publication_year": 2023,
    "research_objective": "Investigating the impact of neural network architectures on image segmentation accuracy",
    "sample_size": 12540
    }
    sys_prompt = f"""
    You are a senior researcher in the field of {field_name}, and you are tasked with accurately extracting key information from an English research paper. Please strictly adhere to the following requirements:
    [Information Extraction Guidelines]
    1. First Author (first_author)
    + Extraction Standard: The full name of the first author in the author list (including middle names/initials if present).
    + Handling Principle: If the first author is marked with "*" indicating the corresponding author, still extract the first author.
    2. Publication Year (publication_year)
    + Timeframe: Identify from the cover, first page, or reference format.
    + Format Requirement: 4-digit year. If no explicit year is found, return null.
    + Special Case: For preprint articles, use the year of the most recent version.
    3. Research Objective (research_objective)
    + Content Standard: Summarize the core research problem in English (12-28 words).
    + Writing Requirement: Use phrases such as "investigate/develop/solve/validate/analyze the impact/mechanism/method of X on Y."
    4. Sample Size (sample_size)
    + Identification Scope: Includes human/animal/data samples, total experimental groups.
    + Format Conversion: Convert expressions like "n=100" to pure numbers.
    + Default Handling: Return null if not explicitly stated.
    [Output Format Requirements]
    1. Strictly use unformatted standard JSON structure.
    2. Fixed field order: first_author → publication_year → research_objective → sample_size.
    3. Use null for empty values (do not use None or nil).
    4. Do not add comments, extra fields, or Markdown syntax.
    Example of Correct Format:
    {output_example}
    Please process the paper content and return only the JSON object that meets the above requirements.    
    """
    return sys_prompt