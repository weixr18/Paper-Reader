import os
from openai import OpenAI
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
from transformers import AutoTokenizer
from f_params import api_settings

def get_sys_prompt(field_name):
    json_format = '{"short_summary": "XXX(短总结)", "summary": "XXXXXX(长总结)"}'
    sys_prompt = f"""
    你是一个{field_name}领域的专家，你将阅读一篇该领域的英文论文。
    首先，请用一句话(中文)简明扼要的总结该领域内该论文的贡献，如"提出了一种SOTA的多线程并行SLAM系统"，称为"短总结"，不超过30字。
    其次，请用中文总结该论文的**研究背景、针对问题、主要方法和结论**，称为"长总结"，注意以下几点：
    + 字数在150-200字之间
    + 确保语言简洁明了，突出论文的重点贡献
    + 不要只看Abstract部分，要同时关注论文正文
    + 常用的英文学术词汇如SLAM,prompt不用翻译
    最后，将提取到的信息以如下的json格式输出：{json_format}
    输出时，只输出我要求的内容，不要输出其他任何内容。
    """
    return sys_prompt


WORK_DIR = os.path.dirname(os.path.abspath(__file__)) + "/.."


def get_model_tknz(PROVIDER):
    # model
    print("Using provider:", PROVIDER)
    def get_properties(provider):
        p = api_settings[provider]
        return p["MODEL"], p["API_KEY"], p["BASE_URL"]
    MODEL, API_KEY, BASE_URL = get_properties(PROVIDER)
    model = OpenAI(api_key = API_KEY, base_url = BASE_URL)
    setattr(model, "provider", PROVIDER)
    setattr(model, "MODEL", MODEL)
    # tokenizer
    tknz_path = os.path.join(WORK_DIR, "src/dpsk_tokenizer")
    tokenizer = AutoTokenizer.from_pretrained( 
        tknz_path, trust_remote_code=True
    )
    # print("Got LLM model and tokenizer.")
    return model, tokenizer


def get_pdf_paths(paper_dir):
    import os, glob
    pdf_files = glob.glob(os.path.join(paper_dir, '**/*.pdf'), recursive=True)
    pdf_path_list = [os.path.abspath(pdf_file) for pdf_file in pdf_files]
    return pdf_path_list


def get_pdf_str(pdf_path):
    from pdfminer.high_level import extract_text
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    txt_path = f"{WORK_DIR}/txt/{pdf_name}.txt"
    if os.path.exists(txt_path):
        with open(txt_path, 'r', encoding='utf-8') as file:
            pdf_str = file.read()
    else:
        pdf_str = extract_text(pdf_path)
        with open(txt_path, 'w', encoding='utf-8') as file:
            file.write(pdf_str)
    return pdf_str


def save_res(res:dict, save_name:str):
    import json
    json_str = json.dumps(res, ensure_ascii=False, indent=4)
    output_file = f'{WORK_DIR}/output/{save_name}.txt'
    with open(output_file, "a", encoding="utf-8") as f:
        f.writelines(json_str)
    pass

