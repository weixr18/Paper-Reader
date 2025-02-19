from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from utils import *
from f_params import *

DEBUG_MODE = False
if DEBUG_MODE:
    paper_dirs = DEBUG_PAPER_DIRS
else:
    paper_dirs = PAPER_DIRS


PROVIDER = "aliyun"
input_price = 2 / 1e6 # ￥2 / 1M token
MAX_WORKERS = 6

def count_tokens(tokenizer):
    pdf_path_list = []
    for paper_dir, _, _ in PAPER_DIRS:
        tmp_list = get_pdf_paths(paper_dir)
        print(f"{paper_dir}: {len(tmp_list)}")
        pdf_path_list += tmp_list
    
    if DEBUG_MODE:
        total_tokens = 0
        for pdf_path in tqdm(pdf_path_list):
            pdf_str = get_pdf_str(pdf_path)
            total_tokens += len(tokenizer.encode(pdf_str))
    else:
        def process_pdf(pdf_path):
            pdf_str = get_pdf_str(pdf_path)
            return len(tokenizer.encode(pdf_str))
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor: 
            futures = [executor.submit(process_pdf, pdf_path) for pdf_path in pdf_path_list]
            results = []
            for future in tqdm(as_completed(futures), total=len(futures)):
                results.append(future.result)
            total_tokens = sum(results)
    print(f"Token num: {total_tokens}, price: {total_tokens*input_price:.4f}")


if __name__ == "__main__":
    _, tokenizer = get_model_tknz(PROVIDER)
    count_tokens(tokenizer)
    