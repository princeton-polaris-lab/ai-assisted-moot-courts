from models import BaseModel

class SandboxModel(BaseModel):
    def __init__(self, api_key: str):
        from portkey_ai import Portkey
        self.client = Portkey(api_key=api_key)

    def generate(self, messages: list, greedy_generation: bool) -> str:
        if greedy_generation:
            response = self.client.chat.completions.create(
                model="gpt-5",
                messages=messages
            )
        else:
            response = self.client.chat.completions.create(
                model="gpt-5",
                messages=messages
            )
        return response.choices[0].message.content
