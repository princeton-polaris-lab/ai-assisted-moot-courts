import pandas as pd
from models.base import get_model
import hydra
from omegaconf import DictConfig, OmegaConf
import utils.main_utils as utils

DATABASE_PATH = "data/adversarial_metrics_decorum_set.db"
GET_CASES_QUERY = "SELECT * FROM transcript_and_all_context WHERE transcript_id<>'2024.23-1239';" # 23-1239 case facts trigger OPENAI's violence filter
ADD_REMARK_QUERY = "INSERT INTO advocate_remark (advocate_remark_id, model, prompting_strategy, advocate, " \
                        "remark_text, log_id, context_id) VALUES (?, ?, ?, ?, ?, ?, ?);"
ADVOCATE_GENERATION_SET_NUM = 6

@hydra.main(version_base=None, config_path="conf/", config_name="make_adversarial_set")
def make_adversarial_set(cfg: DictConfig) -> None:
    if cfg.model_type == 'openai' and not cfg.api_key:
        raise ValueError("api-key is required for OpenAI model")

    model = get_model(cfg.model_type, model_path=cfg.model_path, api_key=cfg.api_key, num_gpus=cfg.num_gpus)
    prompting_strategies = OmegaConf.to_container(cfg.prompting_strategies)

    # open the metrics database view that contains all case information
    conn, cursor = utils.connect_to_db(DATABASE_PATH)
    cases_df = pd.read_sql_query(GET_CASES_QUERY, conn)
    
    additional_remarks = []
    for prompt_idx, strategy in enumerate(prompting_strategies):
        # random seed is index of prompting strategies
        subset_cases_df = cases_df.sample(ADVOCATE_GENERATION_SET_NUM, replace=False, random_state=prompt_idx)
        subset_cases_df = subset_cases_df.reset_index(drop=True)
        for index, row in subset_cases_df.iterrows():
            generated_remark = model.generate_advocate_remark(prompting_strategy=strategy,
                                                       facts=row["case_facts"],
                                                       legal_question=row["legal_question"],
                                                       advocate=row["advocate"],
                                                       context=row["context"])

            model_name = utils.get_model_name(cfg.model_type, cfg.model_path)
            log_id = utils.get_log_id()
            remark_id = utils.make_remark_or_metric_id(model_name, strategy)
            additional_remarks.append((remark_id, model_name, strategy, row["advocate"], generated_remark, 
                                       log_id, row["context_id"]))
        
            if index % 5 == 4 or index == len(subset_cases_df) - 1:
                cursor.executemany(ADD_REMARK_QUERY, additional_remarks)
                conn.commit()
                additional_remarks = []
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    make_adversarial_set()
