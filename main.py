import ollama
from pre_prompt import pre_prompt1, pre_prompt2
import pandas as pd
import json
import os
import glob
from concurrent.futures import ThreadPoolExecutor
import logging

#####config#####
model_name = 'llama3.1' 
max_workers = 2
################

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def use_llm1(input_context):
    response = ollama.generate(model=model_name, prompt=pre_prompt1 + input_context)
    logger.debug(response['response'])
    return response['response']

def use_llm2(model, prompt):
    response = ollama.generate(model=model, prompt=prompt)
    raw_response = response['response']
    
    json_start = raw_response.find('[')
    json_end = raw_response.rfind(']') + 1
    if json_start != -1 and json_end != -1:
        json_str = raw_response[json_start:json_end]
        try:
            json_data = json.loads(json_str)
            logger.debug(f"Parsed JSON data: {json_data}")
            return json_data
        except json.JSONDecodeError:
            logger.error("Error parsing JSON from model response")
            return None
    else:
        logger.error("No valid JSON found in model response")
        return None

def use_llm(input_context):
    result1 = use_llm1(input_context)
    result2 = use_llm2(model=model_name, prompt=pre_prompt2 + result1)
    return result2 if result2 else []

def process_data_file(file_path):
    logger.info(f"Processing file: {file_path}")
    file_name, file_extension = os.path.splitext(file_path)
    
    try:
        if file_extension == '.xlsx':
            df = pd.read_excel(file_path)
        elif file_extension == '.csv':
            df = pd.read_csv(file_path)
        else:
            logger.error(f"Unsupported file type: {file_extension}. Only xlsx and csv are supported.")
            return
        
        results = []
        for i, row in df.iterrows():
            # 将所有列的数据合并为一个字符串
            all_data = ' '.join(row.astype(str).values)
            result_json = use_llm(all_data)
            logger.info(f"Finished processing row {i+1} in file {file_path}")
            if result_json:
                results.extend(result_json)

        json_file = file_name + '_processed.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Finished processing file: {file_path}")
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {str(e)}")

def main():
    data_dir = './data/'
    file_patterns = ['*.csv', '*.xlsx']
    all_files = []
    for pattern in file_patterns:
        all_files.extend(glob.glob(os.path.join(data_dir, pattern)))
    
    logger.info(f"Found {len(all_files)} files to process")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(process_data_file, all_files)

    logger.info("All files have been processed.")

if __name__=="__main__":
    main()