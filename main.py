import ollama

model_name = 'qwen2' 
prompt='''

'''
def use_llm():
    response = ollama.generate(model=model_name, prompt=prompt)
    print(response['response'])
    
if __name__=="__main__":
    use_llm()