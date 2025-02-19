# Paper-Reader

LLM快速阅读+总结论文的工具

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
```

3. 运行`cd src && python3 count_tokens.py`，可以提前了解需要耗费多少token。这里调用的是deepseek官方提供的本地tokenizer，需要使用CPU进行运算，速度较慢。该过程也会将pdf提取出的文本缓存在txt文件中。
4. 运行`cd src && python3 read_papers.py`，调用LLM进行论文阅读，输出结果以json格式存储在`./output/output_file_name_x.txt`中
5. 如有其他信息提取需求，修改`src/utils.py`中的`get_sys_prompt`函数的prompt即可。
