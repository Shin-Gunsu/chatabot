from openai import OpenAI
import sys
import os
file_path = os.path.dirname(__file__) 
sys.path.append(file_path+'../../')
from utils.GetAnswer_assistant import GetAnswer_assistant
from config.GlobalParams import gptapi_key

assistant_model = GetAnswer_assistant(OpenAI(api_key=gptapi_key))
while True:
    print("질문 : ")
    query = input()  # 질문 입력
    if(query == "exit"):
        exit(0)
    print("-" * 40)
    assistant_model.create_thread()
    answer = assistant_model.ask(query)
    assistant_model.end_QnA()
    print(answer)
