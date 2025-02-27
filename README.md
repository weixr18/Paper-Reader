# Paper-Reader

调用LLM API批量总结论文的工具

A tool for batch summarization of research papers using LLM API.

contact: weixr0605@sina.com

## 使用方法

1. 新建路径 `./output` `./txt`
2. 在`./src`下新建文件`f_params.py`，输入以下内容

```py
api_settings = {
    "aliyun": {
        "MODEL": "deepseek-v3",
        "API_KEY": "YOUR_API_KEY", # 更换为你的API_KEY
        "BASE_URL": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    }, 
    # 也可以添加其他厂商的配置，只需在代码文件中修改PROVIDER即可
}


PAPER_DIRS = [
    ("path/1/to/your/paper/pdf/files", "research field 1", "output_file_name_1"),
    ("path/2/to/your/paper/pdf/files", "research field 2", "output_file_name_2"),
] # 默认会对子文件夹下的pdf也进行处理，如不需要可修改utils.py中get_pdf_paths函数
DEBUG_PAPER_DIRS = [
    ("path/to/your/paper/pdf/files", "research field", "output_file_name"),
] # 调试用的配置，可以单独搞一个调试文件夹
CACHE_PATH = "path/to/_cache_" # 存放txt缓存的文件路径
```

3. 运行`python3 src/count_tokens.py`，可以提前了解需要耗费多少输入token。这里调用的是deepseek官方提供的本地tokenizer，需要使用CPU进行运算，速度较慢。该过程也会将pdf提取出的文本缓存在txt文件中。输出token无法提前预测，正常情况下应该比论文全文少很多。
4. 运行`python3 src/read_papers.py`，调用LLM进行论文阅读，输出结果以json格式存储在`./output/output_file_name_x.txt`中
5. 如有其他信息提取需求，可在`src/prompt.py`中增加自己的prompt，并修改`src/read_papers.py`61行的调用。

## Usage Instructions

1. Create the directories `./output` and `./txt`.
2. Create a new file `f_params.py` under `./src` and enter the following content:

```py
api_settings = {
    "aliyun": {
        "MODEL": "deepseek-v3",
        "API_KEY": "YOUR_API_KEY", # Replace with your API_KEY
        "BASE_URL": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    }, 
    # You can also add configurations for other providers(e.g. OpenAI), just modify PROVIDER in the code file
}

PAPER_DIRS = [
    ("path/1/to/your/paper/pdf/files", "research field 1", "output_file_name_1"),
    ("path/2/to/your/paper/pdf/files", "research field 2", "output_file_name_2"),
] # By default, PDFs in subdirectories will also be processed. Modify the get_pdf_paths function in utils.py if this is not needed.
DEBUG_PAPER_DIRS = [
    ("path/to/your/paper/pdf/files", "research field", "output_file_name"),
] # Configuration for debugging, you can set up a separate debug folder.
CACHE_PATH = "path/to/_cache_" # txt cache will be put here
```

3. Run `python3 src/count_tokens.py` to estimate the number of input tokens required in advance. This script uses the official DeepSeek local tokenizer, which runs on the CPU and may be slow. The process also caches extracted text from PDFs into TXT files. The number of tokens cannot be predicted precisely, but it should generally be much lower than the full text of the paper.
4. Before running following code, change `from prompt import *` to `from prompt_eng import *` in `src/read_papers.py`
5. Run `python3 src/read_papers.py` to use the LLM for reading papers. The results will be stored in JSON format in `./output/output_file_name_x.txt`.
6. If you need to extract additional information, you can add your own prompts in `src/prompt_eng.py` and modify line 61 in `src/read_papers.py` accordingly.
