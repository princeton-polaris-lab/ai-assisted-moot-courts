from models import BaseModel
import re

# Assumes we're running with gptoss env
class SglangModel(BaseModel):
    def __init__(self, num_gpus=2):
        import sglang as sgl
        from transformers import AutoTokenizer

        # Always load in my gpt-oss-120b path
        model_path = "YOUR_GPT_OSS_120B_MODEL"
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.llm = sgl.Engine(
            model_path=model_path,
            tp_size=num_gpus,
            trust_remote_code=True,
        )
    
    def parse_response_for_remark(self, text: str) -> str:
        pattern = re.escape("assistantfinal") + r".*?(.*)"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text

    def generate(self, messages: list, greedy_generation: bool) -> str:
        # set generation parameters
        SAMPLING_PARAMS = {
            "max_new_tokens": 16000,
            "n": 1,
            "temperature": 0.7,
        }
        if not greedy_generation:
            SAMPLING_PARAMS["temperature"] = 0.7
        
        # format messages for gpt-oss
        messages[0]["content"] += "Be concise and realistic. Reasoning: high"
        formatted_prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        response = self.llm.generate(
            [formatted_prompt],
            sampling_params=SAMPLING_PARAMS,
            return_logprob=False,
        )

        # remark = self.parse_response_for_remark(response[0]["text"])
        return response[0]["text"]
