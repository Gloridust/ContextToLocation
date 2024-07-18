import os
import csv
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    return chardet.detect(raw_data)['encoding']

def convert_csv_encoding(input_file, output_file, input_encoding, output_encoding='utf-8'):
    with open(input_file, 'r', encoding=input_encoding, errors='replace') as infile, \
         open(output_file, 'w', encoding=output_encoding, newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for row in reader:
            writer.writerow(row)

def process_csv_files(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith('.csv'):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, f'converted_{filename}')
            
            detected_encoding = detect_encoding(input_path)
            print(f"检测到 {filename} 的编码为: {detected_encoding}")
            
            convert_csv_encoding(input_path, output_path, detected_encoding)
            print(f"已将 {filename} 转换为 UTF-8 编码并保存为 {output_path}")

# 使用示例
input_dir = 'path/to/input/directory'  # 替换为您的输入目录路径
output_dir = 'path/to/output/directory'  # 替换为您想要保存转换后文件的目录路径

process_csv_files(input_dir, output_dir)