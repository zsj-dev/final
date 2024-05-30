

import json
import os
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage
)


def predict_by_model(model,prompt):
    res = []
    resp = model.predict_messages([
        SystemMessage(content="Continue writing the following Java code so that it can be concatenated into the original code and run directly."),
        HumanMessage(content=prompt),
    ])
    res.append(resp.content)
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


os.environ["OPENAI_API_KEY"] = 'sk-x1Tf548857Gvrkxr69D1Be7b453e473cB8B9D4D4Eb015dE5'
os.environ["OPENAI_API_BASE"] = 'https://openkey.cloud/v1'
chat = ChatOpenAI(temperature=0,model_name='gpt-3.5-turbo') 


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
            generation = predict_by_model(chat,prompt)
        print("generation finish")
        for text in generation:
            text = clean_reslut(ori,text)
            result = {"task_id": data["task_id"], "generation": text} 
            f_out.write(json.dumps(result) + "\n") 
            f_out.flush() # 实时写入文件 
        index = index+1