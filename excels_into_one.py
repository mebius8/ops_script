# 将directory目录下的所有.xlsx文件合并成一个.xlsx
# 结果输出到当前目录的combined_output.xlsx
# 自主修改变量 directory

import os
import pandas as pd

# 指定Excel文件所在的目录
directory = '/Users/fushaoshan/Documents/lan'

# 创建一个空的DataFrame用于存储合并的数据
combined_df = pd.DataFrame()

# 遍历目录下的所有文件
for filename in os.listdir(directory):
    if filename.endswith(".xlsx") or filename.endswith(".xls"):  # 只处理Excel文件
        file_path = os.path.join(directory, filename)
        # 读取每个Excel文件
        df = pd.read_excel(file_path)
        # 将数据合并到combined_df
        combined_df = pd.concat([combined_df, df], ignore_index=True)

# 将合并的数据写入新的Excel文件

output_file = "combined_output.xlsx"
combined_df.to_excel(output_file, index=False)

print(f"合并完成！文件已保存为 {output_file}")
