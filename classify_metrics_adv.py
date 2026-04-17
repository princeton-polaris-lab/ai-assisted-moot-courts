import pandas as pd
from models.base import get_model
import hydra
from omegaconf import DictConfig, OmegaConf
import utils.main_utils as utils

DATABASE_PATH = "data/adversarial_metrics_decorum_set.db"
GET_CASES_QUERY = "SELECT * FROM remark_transcript_decorum_context_1 WHERE remark_model IN {models_list};"
ADD_METRIC_QUERY = "INSERT INTO adversarial_metrics (adversarial_metric_id, classification_model, metric_name, " \
                            "classification, remark_id, log_id) VALUES (?, ?, ?, ?, ?, ?);"


@hydra.main(version_base=None, config_path="conf/", config_name="classify_metrics")
def metrics_main(cfg: DictConfig) -> None:
    if cfg.model_type in utils.api_models and not cfg.api_key:
        raise ValueError("api-key is required for Sandbox model")

    model = get_model(cfg.model_type, model_path=cfg.model_path, api_key=cfg.api_key, num_gpus=cfg.num_gpus)
    metrics_list = OmegaConf.to_container(cfg.metrics_to_classify)
    remark_models_list = OmegaConf.to_container(cfg.model_ids)

    # open the metrics database view that contains all case information
    conn, cursor = utils.connect_to_db(DATABASE_PATH)
    cases_df = pd.read_sql_query(GET_CASES_QUERY.format(models_list=utils.make_sql_list(remark_models_list)), conn) 

    additional_metrics = []
    for index, row in cases_df.iterrows():
        if index < int(cfg.idx_to_start_run):
            continue
        for metric_title in metrics_list:
            reformatted_context = utils.incorporate_facts_to_context(row["case_facts"], row["legal_question"], row["context"])
            generated_classification = model.classify_metric(classifier_name=metric_title, 
                                                     context=reformatted_context, 
                                                     justice=row["justice"], 
                                                     remark=row["remark_text"])

            model_name = utils.get_model_name(cfg.model_type, cfg.model_path)
            log_id = utils.get_log_id()
            metric_id = utils.make_remark_or_metric_id(model_name, metric_title)
            additional_metrics.append((metric_id, model_name, metric_title, generated_classification, 
                                       row["justice_response_id"], log_id))
        
        # insert into DB every 10 questions (40 runs) or at the end of processing
        if index % 50 == 49 or index == len(cases_df) - 1:
            cursor.executemany(ADD_METRIC_QUERY, additional_metrics)
            conn.commit()
            additional_metrics = []
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    metrics_main()