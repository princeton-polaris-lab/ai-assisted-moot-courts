import ast
import prompts.prompt_templates as prompts
import prompts.automated_metrics as automated_metrics
import prompts.question_generation as question_generation
import prompts.adversarial_generation as adversarial_generation
import utils.prompt_utils as prompt_utils
from abc import ABC, abstractmethod
import re

def get_last_turn_in_context(context: str) -> str:
    context_list = ast.literal_eval(context)
    return str(context_list[-1])


def get_metrics_prompt(metric_name: str, context: str, justice: str, remark: str, remark2: str) -> str:
    # get system prompt from metric name; template type is stored in metric metadata
    metric_metadata = automated_metrics.METRICS_METADATA[metric_name]
    template = prompts.METRIC_TEMPLATES[metric_metadata["metric_type"]]

    system_prompt = template.format(
        classifier_name=metric_name,
        prompt=metric_metadata["prompt"],
        instructions=metric_metadata["instructions"],
        buckets=metric_metadata["buckets"]
    )

    last_advocate_remark = get_last_turn_in_context(context)

    # assume default metric is distributional
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": f"""context: {context}\njustice: {justice}\nlast_advocate_remark: {last_advocate_remark}\ncurrent_judge_turn: {remark}"""}]

    # add the second remark to the prompt if the metric is comparative
    if metric_metadata["metric_type"] == "binary_classification":
        messages[1]["content"] += f"""specific_logical_fallacy: {remark2}"""
    elif metric_metadata["metric_type"] == "comparative":
        messages[1]["content"] += f"""issue: {remark2}"""

    return messages


def get_question_generation_prompt(prompting_strategy: str, facts: str, legal_question: str, justice: str, context: str):
    question_generation_metadata = question_generation.QUESTION_GENERATION_METADATA[prompting_strategy]
    question_generation_template = prompts.QUESTION_GENERATION_PROMPT

    system_prompt = question_generation_template.format(
            role=question_generation_metadata["role"].format(
            justice_name=justice,
            justice_profile=prompt_utils.JUSTICE_PROFILES[justice]
        ),
        facts_of_the_case=facts,
        legal_question=legal_question,
        emphasis=question_generation_metadata["emphasis"]
    )

    return [{"role": "system", "content": system_prompt},
            {"role": "user", "content": f"""Transcript of the oral argument up until the current turn: {context}"""}]


def get_advocate_remark_prompt(prompting_strategy: str, facts: str, legal_question: str, advocate: str, context: str):
    adversarial_remark_metadata = adversarial_generation.ADVERSARIAL_GENENERATION_METADATA[prompting_strategy]
    advocate_remark_template = prompts.ADVOCATE_REMARK_GENERATION_PROMPT                                                                                 

    system_prompt = advocate_remark_template.format(
        role=adversarial_remark_metadata["role"],
        task=adversarial_remark_metadata["task"],
        specification_examples=adversarial_remark_metadata["specification_examples"]
    )

    return [{"role": "system", "content": system_prompt},
            {"role": "user", "content": f"""Facts: {facts}\nLegal Question: {legal_question}\n Context: {context} Attorney: {advocate}"""}
    ]


def postprocess_remark(text: str) -> str:
    if not text:
        return text
    text = re.sub(r'^(<[^>]+>|[\w\s]+):\s*', '', text)
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    text = re.sub(r'^["\']|["\']$', '', text)
    text = re.sub(r'^\*\*[^:]+:\*\*\s*', '', text)
    return text.strip()


def postprocess_metric(text: str) -> str:
    return re.sub(r'^.*?[?:]\s*', '', text)


class BaseModel(ABC):
    @abstractmethod
    def generate(self, prompt: list, greedy_generation: bool) -> str:
        pass

    def classify_metric(self, classifier_name: str, context: str, justice: str, remark: str, remark2=None) -> str:
        messages = get_metrics_prompt(classifier_name, context, justice, remark, remark2)
        response = self.generate(messages, greedy_generation=True)  # calls child class's concrete implementation
        return postprocess_remark(response)
    
    def generate_question(self, prompting_strategy: str, facts: str, legal_question: str, justice: str, context: str):
        messages = get_question_generation_prompt(prompting_strategy, facts, legal_question, justice, context)
        response = self.generate(messages, greedy_generation=True)
        return postprocess_remark(response)
    
    def generate_question_variable(self, prompting_strategy: str, facts: str, legal_question: str, justice: str, context: str, greedy_generation: bool):
        messages = get_question_generation_prompt(prompting_strategy, facts, legal_question, justice, context)
        response = self.generate(messages, greedy_generation=greedy_generation)
        return postprocess_remark(response)

    def generate_advocate_remark(self, prompting_strategy: str, facts: str, legal_question: str, advocate: str, context: str):
        messages = get_advocate_remark_prompt(prompting_strategy, facts, legal_question, advocate, context)
        response = self.generate(messages, greedy_generation=True)
        return postprocess_remark(response)


def get_model(model_type: str, **kwargs) -> BaseModel:
    if model_type == "vllm":
        from models import VllmModel
        return VllmModel(kwargs["model_path"], kwargs["num_gpus"])
    elif model_type == "sandbox":
        from models import SandboxModel
        return SandboxModel(api_key=kwargs["api_key"])
    elif model_type == "sglang":
        from models import SglangModel
        return SglangModel(num_gpus=kwargs["num_gpus"])
    elif model_type == "gemini":
        from models import GeminiModel
        return GeminiModel(api_key=kwargs["api_key"])
    else:
        raise ValueError(f"Unknown model type: {model_type}")
