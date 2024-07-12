import ollama

model_name = 'qwen2-ctl' 
prompt='''
昨夜结束了三天的自驾游旅行（新都-自贡恐龙博物馆-宜宾李庄古镇-蜀南竹海-中国西部大峡谷，行程千余公里）回到了南充，此次旅游总的来说很不错，四家人在一起（三辆车），一边开车一边欣赏沿途的风景，有说有笑其乐融融（驾驶的时候对讲机很起作用哦），就是感觉时间有点紧，一个人驾驶还是有点累！ 
'''

def use_llm():
    response = ollama.generate(model=model_name, prompt=prompt)
    print(response['response'])
    
if __name__=="__main__":
    use_llm()