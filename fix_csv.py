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

def process_csv_files(input_directory):
    output_directory = os.path.join(os.getcwd(), 'fixed')
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for root, dirs, files in os.walk(input_directory):
        for filename in files:
            if filename.endswith('.csv'):
                input_path = os.path.join(root, filename)
                relative_path = os.path.relpath(input_path, input_directory)
                output_path = os.path.join(output_directory, relative_path)
                
                # 确保输出文件的目录存在
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                detected_encoding = detect_encoding(input_path)
                print(f"检测到 {input_path} 的编码为: {detected_encoding}")
                
                convert_csv_encoding(input_path, output_path, detected_encoding)
                print(f"已将 {input_path} 转换为 UTF-8 编码并保存为 {output_path}")

# 使用示例
input_dir = "./"

process_csv_files(input_dir)