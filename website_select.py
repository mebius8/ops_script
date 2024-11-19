# 给定一个excel文件input_file，A列为批量URL（不包含表头）
# 多线程访问并通过关键词ai_keywords判断是否符合要求，并在对应B列输入结果
# 结束后output_file保存到当前目录
# 自主修改变量 input_file，output_file

import requests
from bs4 import BeautifulSoup
import openpyxl
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# 定义一些可能的AI相关英文关键词
ai_keywords = [
    "AI tools", "generative AI", "AI platform",
    "AI tool aggregators", "Ai Aggregator", "AI resources", "AI tools directory", "AI applications"
]
ai_keywords = [keyword.lower() for keyword in ai_keywords]


# 判断网站是否为AI工具聚合网站的函数
def is_ai_aggregation_site(url):
    try:
        # 如果URL没有协议（http或https），则自动添加http://
        if not urlparse(url).scheme:
            url = "http://" + url

        # 获取网页内容
        # print(url)
        response = requests.get(url, timeout=10)  # 设置超时时间为10秒
        response.raise_for_status()  # 如果请求失败会抛出异常

        # 解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取网页文本并进行关键词匹配
        page_text = soup.get_text().lower()
        if any(keyword.lower() in page_text for keyword in ai_keywords):
            print(f"{url} is AI Tool Aggregation Site")
            return f"{url} is AI Tool Aggregation Site"
        else:
            print(f"{url} is Not an AI Tool Aggregation Site")
            return f"{url} is Not an AI Tool Aggregation Site"
    except requests.exceptions.RequestException as e:
        print(f"{url}Request Failed: {e}")
        return f"{url}Request Failed: {e}"


# 处理每一行数据的函数
def process_row(url):
    result = is_ai_aggregation_site(url)
    return result


# 从Excel读取URL并写回结果的函数
def process_urls_from_excel(input_file, output_file):
    # 打开Excel文件
    workbook = openpyxl.load_workbook(input_file)
    sheet = workbook.active

    # 读取所有URL并创建任务
    tasks = []
    for row in sheet.iter_rows(min_row=2, max_col=2):  # 假设第一行是表头，从第二行开始
        url_cell = row[0]
        result_cell = row[1]

        if url_cell.value:  # 检查URL是否为空
            url = url_cell.value.strip()
            tasks.append((url, result_cell))  # 将URL和对应的B列单元格一起存储

    # 创建一个线程池，限制最大线程数为10
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_row, url): result_cell for url, result_cell in tasks}

        # 等待所有任务完成并获取结果
        for future in as_completed(futures):
            result = future.result()
            result_cell = futures[future]
            result_cell.value = result  # 将结果写入对应的B列

    # 保存修改到新文件
    workbook.save(output_file)
    print(f"Results saved to {output_file}")


# 测试代码
input_file = "/Users/fushaoshan/Downloads/failed.xlsx"  # 输入Excel文件
output_file = "failed-check.xlsx"  # 输出结果的Excel文件
process_urls_from_excel(input_file, output_file)