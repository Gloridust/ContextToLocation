import ollama

model_name = 'gemma2' 

pre_prompt1='''
你是一个旅游大数据规划专家，从下面出行计划文本中，规划出旅客对应每个景点的到达时间。如果遇到不确定的数据，通过你的经验推测。以到达地点-时间点的格式，直接输出你的推测结果，其中时间是指你推测的时刻，如：14:00。
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
    
def main():
    input_context='''
    昨夜结束了三天的自驾游旅行（新都-自贡恐龙博物馆-宜宾李庄古镇-蜀南竹海-中国西部大峡谷，行程千余公里）回到了南充，此次旅游总的来说很不错，四家人在一起（三辆车），一边开车一边欣赏沿途的风景，有说有笑其乐融融（驾驶的时候对讲机很起作用哦），就是感觉时间有点紧，一个人驾驶还是有点累！ 
    '''
    result_json=use_llm(input_context)
    print("result_json>>>"+result_json)

if __name__=="__main__":
    main()