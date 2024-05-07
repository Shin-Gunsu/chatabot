class Ansgpt:
  def __init__(self,model) -> None:
    self.model = model

  def generate_answer(self,query,content):
    
    client = self.model

    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": content},
            {"role": "user", "content": query}
        ]
    )

    return (completion.choices[0].message.content)
