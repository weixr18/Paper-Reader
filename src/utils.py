import os
from openai import OpenAI
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
from transformers import AutoTokenizer
from f_params import api_settings


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

