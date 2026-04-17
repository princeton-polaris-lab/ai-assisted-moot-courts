import pandas as pd
from models.base import get_model
import hydra
from omegaconf import DictConfig, OmegaConf
import utils.main_utils as utils

DATABASE_PATH = "data/opening_statement_set.db"
GET_CASES_QUERY = "SELECT * from transcript_and_os_context;"
ADD_REMARK_QUERY = "INSERT INTO remark (remark_id, model, prompting_strategy, justice, " \
                        "remark_text, log_id, context_id) VALUES (?, ?, ?, ?, ?, ?, ?);"

justice_list = ['Clarence Thomas', 'Ketanji Brown Jackson', 'Elena Kagan',
       'Amy Coney Barrett', 'Brett M. Kavanaugh', 'John G. Roberts, Jr.',
       'Neil Gorsuch', 'Sonia Sotomayor', 'Samuel A. Alito, Jr.']

@hydra.main(version_base=None, config_path="conf/", config_name="generate_questions")
def question_gen_main(cfg: DictConfig) -> None:
    if cfg.model_type in utils.api_models and not cfg.api_key:
        raise ValueError("api-key is required for API models")

    model = get_model(cfg.model_type, model_path=cfg.model_path, api_key=cfg.api_key, num_gpus=cfg.num_gpus)
    prompting_strategies = OmegaConf.to_container(cfg.prompting_strategies)

    # open the metrics database view that contains all case information
    conn, cursor = utils.connect_to_db(DATABASE_PATH)
    cases_df = pd.read_sql_query(GET_CASES_QUERY, conn)
    cases_df = cases_df.sample(n=30, random_state=42).reset_index(drop=True)
    
    additional_remarks = []
    for index, row in cases_df.iterrows():
        for strategy in prompting_strategies:
            for justice in justice_list:
                generated_remark = model.generate_question(prompting_strategy=strategy,
                                                        facts=row["case_facts"],
                                                        legal_question=row["legal_question"],
                                                        justice=justice,
                                                        context=row["context"])
                model_name = utils.get_model_name(cfg.model_type, cfg.model_path)
                log_id = utils.get_log_id()
                remark_id = utils.make_remark_or_metric_id(model_name, strategy)
                additional_remarks.append((remark_id, model_name, strategy, justice, generated_remark, 
                                        log_id, row["os_context_id"]))
            
                # insert into DB every 10 questions (90 runs) or at the end of processing
                if index % 10 == 9 or index == len(cases_df) - 1:
                    cursor.executemany(ADD_REMARK_QUERY, additional_remarks)
                    conn.commit()
                    additional_remarks = []
    cursor.close()
    conn.close()

if __name__ == "__main__":
    question_gen_main()
