import ollama
import pandas as pd
import json
import os

model_name = 'gemma2' 

pre_prompt1='''
你是一个旅游大数据规划专家，从下面出行计划文本中，规划出自驾旅客对应每个景点的到达时间。如果遇到不确定的数据，通过你的经验推测。以到达地点-时间点的格式，直接输出你的推测结果，其中时间是指你推测的时刻，如：14:00。
'''

pre_prompt2='''
You are a data processing robot. Your function is to extract the exact time and location of a person's arrival at a certain location from a text from social media and output it in json format.
If you are unsure, you can infer a reasonable time during the day, which must be in HH:MM format.
This time must be reasonable. Based on your experience, what time of day is he likely to visit here.
Be sure to figure out the exact time of day, such as 12:00, not other text, which must be in the format of HH:MM;
You need to consider that this time must be reasonable. Based on your experience, what time of day he might visit here?
In other words, you must output All data in json, start outputting directly, and don't output anything else. Here is an example:
{
"location":"Chengdu People's Park",
"time":"12:00"
},
{
"location":"Chengdu Museum",
"time":"14:00"
},

Below, you will receive the information you need to process:
'''


def use_llm1(input_context):
    response = ollama.generate(model=model_name, prompt=pre_prompt1 + input_context)
    print(response['response'])
    return response['response']

def use_llm2(model, prompt):
    response = ollama.generate(model=model, prompt=prompt)
    print(response['response'])
    return response['response']

def use_llm(input_context):
    result1 = use_llm1(input_context)
    result2 = use_llm2(model=model_name, prompt=pre_prompt2 + result1)
    return result2

def process_data_file(file_path):
    file_name, file_extension = os.path.splitext(file_path)
    
    if file_extension == '.xlsx':
        df = pd.read_excel(file_path)
    elif file_extension == '.csv':
        df = pd.read_csv(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}. Only xlsx and csv are supported.")
    
    if 'description' not in df.columns:
        raise ValueError("Column 'description' not found in the data.")
    
    descriptions = df['description'].tolist()
    
    results = []
    for description in descriptions:
        result_json = use_llm(description)
        results.append(result_json)

    json_file = file_name + '.json'
    with open(json_file, 'a', encoding='utf-8') as f:
        for result in results:
            json.dump(result, f, ensure_ascii=False)
            f.write('\n')
            
def main():
    file_path = './data/wb-chengdu-city.csv'
    process_data_file(file_path)

if __name__=="__main__":
    main()