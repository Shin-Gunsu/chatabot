import sys
import os
file_path = os.path.dirname(__file__)  # 현재 파일의 절대 경로를 가져옵니다.
sys.path.append(file_path+'../../')
from GlobalParams import assistant_id
from GlobalParams import file_id

class GetAnswer_assistant:
    def __init__(self,client):
        self.client = client
        self.assistant = assistant_id
        self.message_file_id = file_id
        self.thread_id = ""

    def create_thread(self):
        thread = self.client.beta.threads.create()
        self.thread_id = thread.id
    

    def ask(self,query):
        thread_message = self.client.beta.threads.messages.create(
          self.thread_id,
          role="user",
          content=query,
          attachments=[{ "file_id": self.message_file_id, "tools": [{"type": "file_search"}] }]
        )
        run = self.client.beta.threads.runs.create_and_poll(
          thread_id=self.thread_id, assistant_id=self.assistant
        )
        messages = list(self.client.beta.threads.messages.list(thread_id=self.thread_id, run_id=run.id))
        message_content = messages[0].content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
          message_content.value = message_content.value.replace(annotation.text,"").rstrip('.')
          if file_citation := getattr(annotation, "file_citation", None):
            cited_file = self.client.files.retrieve(file_citation.file_id)
            citations.append(f"[{index}] {cited_file.filename}")
        return message_content.value
    
    def end_QnA(self):
      self.client.beta.threads.delete(self.thread_id)
       