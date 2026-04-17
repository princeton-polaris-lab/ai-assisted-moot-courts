import pandas as pd
from models.base import get_model
import hydra
from omegaconf import DictConfig, OmegaConf
import utils.main_utils as utils

# Can change database path to issue_coverage_specific
DATABASE_PATH = "data/issue_coverage_broad.db"
GET_CASES_QUERY = "SELECT * FROM transcript_issue_remark WHERE model IN {models_list};"
ADD_METRIC_QUERY = "INSERT INTO coverage_metrics (coverage_metric_id, model_name, metric_title, issue_id, remark_id, " \
                            "addresses_issue, log_id) VALUES (?, ?, ?, ?, ?, ?, ?);"


@hydra.main(version_base=None, config_path="conf/", config_name="classify_metrics")
def metrics_main(cfg: DictConfig) -> None:
    if cfg.model_type in utils.api_models and not cfg.api_key:
        raise ValueError("api-key is required for Sandbox model")

    model = get_model(cfg.model_type, model_path=cfg.model_path, api_key=cfg.api_key, num_gpus=cfg.num_gpus)
    metrics_list = OmegaConf.to_container(cfg.metrics_to_classify)

    # open the metrics database view that contains all case information
    conn, cursor = utils.connect_to_db(DATABASE_PATH)
    remark_models_list = OmegaConf.to_container(cfg.model_ids)
    cases_df = pd.read_sql_query(GET_CASES_QUERY.format(models_list=utils.make_sql_list(remark_models_list)), conn) 

    additional_metrics = []
    for index, row in cases_df.iterrows():
        for metric_title in metrics_list:
            reformatted_context = utils.incorporate_facts_to_context(row["case_facts"], row["legal_question"], row["context"])
            generated_classification = model.classify_metric(classifier_name=metric_title, 
                                                     context=reformatted_context, 
                                                     justice=row["justice"], 
                                                     remark=row["remark_text"],
                                                     remark2=row["issue_label"])

            model_name = utils.get_model_name(cfg.model_type, cfg.model_path)
            log_id = utils.get_log_id()
            metric_id = utils.make_remark_or_metric_id(model_name, metric_title)
            additional_metrics.append((metric_id, model_name, metric_title, row["issue_id"], row["remark_id"], 
                                       generated_classification, log_id))
        
        # insert into DB every 10 questions (40 runs) or at the end of processing
        if index % 50 == 49 or index == len(cases_df) - 1:
            cursor.executemany(ADD_METRIC_QUERY, additional_metrics)
            conn.commit()
            additional_metrics = []
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    metrics_main()