
import re
from datetime import datetime
import hashlib
import hydra
import sqlite3
import ast

api_models = ["sandbox", "gemini"]

def make_remark_or_metric_id(model_name, remark_or_metric_title):
    unique_string = f"{model_name}_{remark_or_metric_title}_{datetime.now()}"
    return hashlib.md5(unique_string.encode()).hexdigest()

def get_model_name(model_type, model_path):
    if model_type == "sandbox":
        return "gpt4o"
    elif model_type == "sglang":
        return "gpt-oss-120b"
    elif model_type == "gemini":
        return "gemini-2.5-pro"
    # model is local
    return re.search(r'transformer_cache/(.+)', model_path).group(1)

def get_log_id():
    hydra_cfg = hydra.core.hydra_config.HydraConfig.get()
    logging_dir = hydra_cfg['runtime']['output_dir']
    # log_id might can start with 'output/' or 'multiturn/'
    return re.search(r'oral-args-metrics/(.+)', logging_dir).group(1)

def connect_to_db(database_path: str):
    conn = sqlite3.connect(database_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()
    return conn, cursor

def make_sql_list(values):
    # returns string, bookmarked with parentheses, of sqlite search 
    # with remark_log_ids as data
    sql_list_str = "("
    for i, value in enumerate(values):
        sql_list_str += f"\'{value}\'"
        if i < len(values) - 1:
            sql_list_str += ", "
    sql_list_str += ')'
    return sql_list_str

def incorporate_facts_to_context(case_facts, legal_question, context):
    context_list = ast.literal_eval(context)
    system_prompt = {'content': f"""You are a legal expert trained to simulate Supreme Court oral arguments.\n\nFACTS_OF_THE_CASE:\n{case_facts}\n\nLEGAL_QUESTION:\n{legal_question}""",
    'role': 'system'}
    context_list.insert(0, system_prompt)
    return str(context_list)