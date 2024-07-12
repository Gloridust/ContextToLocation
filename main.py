import ollama

model_name = 'qwen2-ctl' 
pre_prompt='''
You are a text processing robot. Your function is to extract the time and place of a person's arrival at a certain location from a text from social media and output it in json format. If the exact time is not mentioned, then infer an approximate arrival time through his description; if there are multiple locations, output multiple; if there is no time or location at all, then just output a line break. In other words, you can only output data or line breaks in json format, start outputting directly, and don't output anything else. Here is an example:
{
"location":"Chengdu People's Park"
"time":"12:00"
}
{
"location":"Chengdu Museum"
"time":"14:00"
}

Below, you will receive the information you need to process:
'''

input_context='''
昨夜结束了三天的自驾游旅行（新都-自贡恐龙博物馆-宜宾李庄古镇-蜀南竹海-中国西部大峡谷，行程千余公里）回到了南充，此次旅游总的来说很不错，四家人在一起（三辆车），一边开车一边欣赏沿途的风景，有说有笑其乐融融（驾驶的时候对讲机很起作用哦），就是感觉时间有点紧，一个人驾驶还是有点累！ 
'''

prompt=pre_prompt+input_context

def use_llm():
    response = ollama.generate(model=model_name, prompt=prompt)
    print(response['response'])
    
if __name__=="__main__":
    use_llm()