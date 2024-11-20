# 给定一个excel文件file_path，A列为基础数据，B列为待对比数据，不包含表头
# 清洗AB列数据，并将B列中每个url同A列所有数据做对比，若重复则在对应C列输入1
# 结果output_path保存到当前目录
# 自主修改变量 file_path，output_path

import pandas as pd

# 加载 Excel 文件
file_path = '/Users/fushaoshan/Downloads/已有AI_tools_site_重复对比.xlsx'
data = pd.ExcelFile(file_path)

# 加载第一个工作表的数据
df = data.parse('Sheet1')

# 定义标准化网址的函数（移除协议、'www.'、尾部斜杠等）
def standardize_url(url):
    if pd.isna(url):  # 处理缺失值
        return None
    url = url.lower()
    url = url.replace("http://", "").replace("https://", "").replace("www.", "").strip(" ").strip("/")
    return url

# 标准化 A 列和 B 列中的网址
df['standardized_A'] = df['A'].apply(standardize_url)
df['standardized_B'] = df['B'].apply(standardize_url)

# 检查 B 列每一项在 A 列中是否有重复
# 如果 B 列为空白，则 C 列输出为空白
df['C'] = df['standardized_B'].apply(
    lambda x: 1 if pd.notna(x) and x in df['standardized_A'].values else (None if pd.isna(x) else 0)
)

# 删除辅助列以生成干净的输出
output_df = df[['A', 'B', 'C']]

# 保存结果到新文件
output_path = 'processed_duplicates_modified.xlsx'
output_df.to_excel(output_path, index=False)

print(f"处理后的文件已保存到：{output_path}")
