
def get_sys_prompt_summary(field_name):
    # 总结
    json_example = '{"short_summary": "XXX(短总结)", "summary": "XXXXXX(长总结)"}'
    sys_prompt = f"""
    你是一个{field_name}领域的专家，你将阅读一篇该领域的英文论文。
    首先，请用一句话(中文)简明扼要的总结该领域内该论文的贡献，如"提出了一种SOTA的多线程并行SLAM系统"，称为"短总结"，不超过30字。
    其次，请用中文总结该论文的**研究背景、针对问题、主要方法和结论**，称为"长总结"，注意以下几点：
    + 字数在150-200字之间
    + 确保语言简洁明了，突出论文的重点贡献
    + 不要只看Abstract部分，要同时关注论文正文
    + 常用的英文学术词汇如SLAM,prompt不用翻译
    最后，将提取到的信息以如下的json格式输出：{json_example}
    输出时，只输出我要求的内容，不要输出其他任何内容。
    """
    return sys_prompt



def get_sys_prompt_extract(field_name):
    # you can write your own prompt here
    json_example = '{"第一作者": "Wenfeng Liang.", "发表年份": "YYYY", "研究目的": "XXXXXXX", "Filter": "EKF", "Sensors": "None", "Measure": "S-Vector"}'
    sys_prompt = f"""
    你是一个{field_name}领域的专家，你将阅读一篇该领域的英文论文，请你提取以下信息：
    + 第一作者: 排名第一的作者全名
    + 发表年份: 发表的年份，若无年份信息则填入None
    + 研究目的: 该研究主要解决什么方面的问题，用10-30字概括
    + 样本量: 研究使用的样本量，若未指出则填入None
    最后，将提取到的信息以json格式输出，例如：{json_example}
    输出时，只输出我要求的内容，不要输出其他任何内容。
    """
    return sys_prompt
