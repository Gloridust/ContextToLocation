import ollama
import pandas as pd
import json
import os
import glob
from concurrent.futures import ThreadPoolExecutor
import logging

model_name = 'gemma2' 

pre_prompt1='''
你是一个旅游大数据规划专家，从下面出行计划文本中，规划出自驾旅客对应每个景点的到达时间。如果遇到不确定的数据，通过你的经验推测出来。以到达地点-时间点的格式，直接输出你的推测结果，其中时间是指你推测的时刻，如：14:00。
'''

pre_prompt2='''
You are a data processing robot. Your function is to extract the exact time and location of a person's arrival at a certain location and output it in json format.
Be sure to figure out the exact time of day, such as 12:00, not other text, which must be in the format of HH:MM;
You need to consider that this time must be reasonable. Based on your experience, what time of day he might visit there.
Output ONLY valid JSON array, nothing else. Example format:
[
  {
    "location": "Chengdu People's Park",
    "time": "12:00"
  },
  {
    "location": "Chengdu Museum",
    "time": "14:00"
  }
]

Process the following information:
'''

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
        
        if 'description' not in df.columns:
            logger.error(f"Column 'description' not found in the file: {file_path}")
            return
        
        descriptions = df['description'].tolist()
        
        results = []
        for i, description in enumerate(descriptions, 1):
            result_json = use_llm(description)
            logger.info(f"Finished processing row {i} in file {file_path}")
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

    # 使用ThreadPoolExecutor进行多线程处理
    with ThreadPoolExecutor(max_workers=4) as executor:  # 可以根据需要调整max_workers
        executor.map(process_data_file, all_files)

    logger.info("All files have been processed.")

if __name__=="__main__":
    main()