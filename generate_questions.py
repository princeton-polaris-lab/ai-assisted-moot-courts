import pandas as pd
from models.base import get_model
import hydra
from omegaconf import DictConfig, OmegaConf
import utils.main_utils as utils

DATABASE_PATH = "data/distributional_metrics.db"
GET_CASES_QUERY = "SELECT * from transcript_and_context;"
ADD_REMARK_QUERY = "INSERT INTO remark (remark_id, model, prompting_strategy, justice, " \
                        "remark_text, log_id, context_id) VALUES (?, ?, ?, ?, ?, ?, ?);"

@hydra.main(version_base=None, config_path="conf/", config_name="generate_questions")
def question_gen_main(cfg: DictConfig) -> None:
    if cfg.model_type in utils.api_models and not cfg.api_key:
        raise ValueError("api-key is required for API models")

    model = get_model(cfg.model_type, model_path=cfg.model_path, api_key=cfg.api_key, num_gpus=cfg.num_gpus)
    prompting_strategies = OmegaConf.to_container(cfg.prompting_strategies)

    # open the metrics database view that contains all case information
    conn, cursor = utils.connect_to_db(DATABASE_PATH)
    cases_df = pd.read_sql_query(GET_CASES_QUERY, conn)
    
    additional_remarks = []
    for index, row in cases_df.iterrows():
        for strategy in prompting_strategies:
            generated_remark = model.generate_question(prompting_strategy=strategy,
                                                    facts=row["case_facts"],
                                                    legal_question=row["legal_question"],
                                                    justice=row["justice"],
                                                    context=row["context"])

            model_name = utils.get_model_name(cfg.model_type, cfg.model_path)
            log_id = utils.get_log_id()
            remark_id = utils.make_remark_or_metric_id(model_name, strategy)
            additional_remarks.append((remark_id, model_name, strategy, row["justice"], generated_remark, 
                                    log_id, row["context_id"]))
        
            # insert into DB every 20 questions (60 runs) or at the end of processing
            if index % 2 == 1 or index == len(cases_df) - 1:
                cursor.executemany(ADD_REMARK_QUERY, additional_remarks)
                conn.commit()
                additional_remarks = []
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    question_gen_main()
