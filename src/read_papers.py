from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from utils import *
from f_params import *

PROVIDER = "aliyun"
DEBUG_MODE = False
INPUT_PRICE = 1 / 1e6 # 打折期间
OUTPUT_PRICE = 4 / 1e6 # 打折期间

if DEBUG_MODE:
    paper_dir_list = DEBUG_PAPER_DIRS
else:
    paper_dir_list = PAPER_DIRS


def llm_read(model:OpenAI, pdf_path:str, sys_prompt:str, save_name:str):
    import time, json
    pdf_str = get_pdf_str(pdf_path)
    start_time = time.time()
    completion = model.chat.completions.create(
        model="deepseek-v3", 
        messages=[
            {'role': 'system', 'content': sys_prompt},
            {'role': 'user', 'content': pdf_str}
        ],
        max_tokens=2048,
        temperature=1.0,
        stream=False,
    )
    res_str = completion.choices[0].message.content
    llm_json = json.loads(res_str)
    input_tokens = completion.usage.prompt_tokens
    output_tokens = completion.usage.completion_tokens
    price = INPUT_PRICE * input_tokens + OUTPUT_PRICE * output_tokens
    duration = time.time() - start_time
    llm_res = {
        "file": os.path.splitext(os.path.basename(pdf_path))[0],
        "path": os.path.dirname(os.path.abspath(pdf_path)),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "price": price,
        "duration": duration,
    }
    llm_json.update(llm_res)
    save_res(llm_json, save_name)
    return 


MAX_WORKERS = 6

def read_papers(model:OpenAI):    
    for paper_dir, field, save_name in paper_dir_list:
        pdf_path_list = get_pdf_paths(paper_dir)
        print(f"{paper_dir}: {len(pdf_path_list)}")
        sys_prompt = get_sys_prompt(field)
        if DEBUG_MODE:
            for pdf_path in tqdm(pdf_path_list):
                llm_read(model, pdf_path, sys_prompt, save_name)
        else:
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor: 
                futures = [executor.submit(llm_read, model, pdf_path, sys_prompt, save_name) for pdf_path in pdf_path_list]
                results = []
                for future in tqdm(as_completed(futures), total=len(futures)):
                    results.append(future.result)
        print(f"Processing done for {paper_dir}.")
    pass


if __name__ == "__main__":
    model, _ = get_model_tknz(PROVIDER)
    read_papers(model)
    