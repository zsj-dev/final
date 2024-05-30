import json
import requests

# 定义API请求函数
def generate_text(prompt,num):
    res = []
    api_key = "sk-x1Tf548857Gvrkxr69D1Be7b453e473cB8B9D4D4Eb015dE5"
    url = "https://openkey.cloud/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "temperature":0,
        "n":num,
        "messages": [{"role": "system", "content": "You are a Java expert.Continue writing the following Java code so that it can be concatenated into the original code and run directly."},
                    {"role": "user", "content": prompt},]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_json = response.json()
        for i in range(num):
            res.append(response_json["choices"][i]["message"]["content"])
        return res
    except:
        return res
    
def generate_text_with_assistant(ori,prompt,assistant_text,num):
    res = []
    api_key = "sk-x1Tf548857Gvrkxr69D1Be7b453e473cB8B9D4D4Eb015dE5"
    url = "https://openkey.cloud/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    print(ori)
    data = {
        "model": "gpt-3.5-turbo",
        "temperature":0,
        "n":num,
        "messages": [{"role": "system", "content": "You are a Java expert.Continue writing the following Java code so that it can be concatenated into the original code and run directly."},
                     {"role": "user", "content": prompt},
                     {"role": "assistant", "content": assistant_text},
                     {"role": "user", "content": ori},
                     {"role": "assistant", "content": "Therefore, provide the complete code after completion:"},]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_json = response.json()
        for i in range(num):
            res.append(response_json["choices"][i]["message"]["content"])
            print(response_json["choices"][i]["message"]["content"])
        return res
    except:
        return res

def zeroshot_cot(ori,prompt,num):
    res = []
    api_key = "sk-x1Tf548857Gvrkxr69D1Be7b453e473cB8B9D4D4Eb015dE5"
    url = "https://openkey.cloud/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "temperature":0,
        "n":1,
        "messages": [{"role": "user", "content": prompt},
                     {"role": "assistant", "content": "Let's think step by step"}]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_json = response.json()
        print(response_json["choices"][0]["message"]["content"])
        return generate_text("Q: "+prompt+"\nA: Let's think step by step.\n"+response_json["choices"][0]["message"]["content"]+"\nQ: "+ori,num)
    except:
        return res

def clean_declaration(dec):
        strIndex = dec.find("Example")
        if strIndex==0 or strIndex==-1:
            strIndex = dec.find("for example:")
        if strIndex==0 or strIndex==-1:
            strIndex = dec.find("For example:")
        if strIndex==0 or strIndex==-1:
            strIndex = dec.find("example")
        if strIndex==0 or strIndex==-1:
            strIndex = dec.find("Examples")
        if strIndex==0 or strIndex==-1:
            strIndex = dec.find("examples")
        if strIndex==0 or strIndex==-1:
            strIndex = dec.find(">>>")
        if strIndex==0 or strIndex==-1:
            strIndex = dec.find("<p>")
        if not strIndex == -1:
            dec ='    /**\n    '+ dec[:strIndex]+'     */\n    '
        print(dec)
        return dec

def clean_reslut(ori,text):
    start = text.find("```java\n") + len("```java\n")
    end = text.rfind("```")
    if not text.find("```java\n")==-1:
        text=text[start:end]
    text.replace("\n\n","\n")
    ori.replace("\n\n","\n")
    ori = ori[ori.rfind("public"):]
    if not text.find(ori)==-1:
        oriIndex = text.find(ori)+len(ori)
        text = text[oriIndex:]
    return text

def few_shot(prompt,num):
    ex1 = "Q: import java.util.*;\nimport java.lang.*;\n\nclass Solution {\n    public double truncateNumber(double number) {\n\n A:         return number % 1.0;\n    }\n}\n"
    ex2 = "Q: import java.util.*;\nimport java.lang.*;\n\nclass Solution {\n    public int strlen(String string) {\n\n A:         return string.length();\n    }\n}\n"
    ex3 = "Q: import java.util.*;\nimport java.lang.*;\n\nclass Solution {\n    public boolean isEqualToSumEven(int n) {\n\n A:         return n % 2 == 0 && n >= 8;\n    }\n}\n"
    return generate_text(ex1+ex2+ex3+"Q: "+prompt+"\nA: ",num)


with open("humanevalx_java.jsonl", "r") as f_in, open("output.jsonl", "w") as f_out: 
    index = 0 
    cnt = 1
    for line in f_in: 
        print(" "+str(index)+" ") 
        data = json.loads(line.strip()) 
        ori = data["declaration"] 
        prompt = data["prompt"] 
        # dec = clean_declaration(data["text"])
        generation = []
        print("generation")
        while(len(generation)==0):
            generation = zeroshot_cot(ori,prompt,cnt) 
        print("generation finish")
        for text in generation:
            text = clean_reslut(ori,text)
            result = {"task_id": data["task_id"], "generation": text} 
            f_out.write(json.dumps(result) + "\n") 
            f_out.flush() # 实时写入文件 
        index = index+1
