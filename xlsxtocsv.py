import os
import pandas as pd

# 设置目录路径
directory = './data/'

# 遍历目录中的所有文件
for filename in os.listdir(directory):
    if filename.endswith('.xlsx'):
        # 构造完整的文件路径
        file_path = os.path.join(directory, filename)
        
        # 读取Excel文件
        df = pd.read_excel(file_path)
        
        # 构造新的CSV文件名
        csv_filename = os.path.splitext(filename)[0] + '.csv'
        csv_path = os.path.join(directory, csv_filename)
        
        # 将数据框保存为CSV文件
        df.to_csv(csv_path, index=False)
        
        print(f'已将 {filename} 转换为 {csv_filename}')

print('所有 xlsx 文件已成功转换为 csv 格式。')