import ollama

model_name = 'qwen2' 

def use_llm():
    response = ollama.chat(model=model_name, messages=[
    {
        'role': 'user',
        'content': 'Print "hello world" in python',
    },
    ])
    print(response['message']['content'])
    
if __name__=="__main__":
    use_llm()