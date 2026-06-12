## AI-Assisted Moot Courts: Simulating Justice-Specific Questioning in Oral Arguments
This repo contains the code to run experiments for our paper  [AI-Assisted Moot Courts: Simulating Justice-Specific Questioning in Oral Arguments](https://arxiv.org/abs/2603.04718). Our data and results can be found [here](https://huggingface.co/datasets/ai-law-society-lab/oral-args-data-and-results/tree/main).

To run the code, first download the data folder. Your hydra configs will need to point to its path so remember where you saved it. We have two separate environments, one for running gptoss (with sglang), and another for running local models (with vllm). You might want an environment manager to switch between the two of them.

Running experiments is simple. Each run is controlled by one of the python scripts in the root directory. At a high level, each root script grabs a dataset, prompt, and model, conducts inference, and saves the results back to that same sqlite dataset. Prompts are set per python script. You can change the dataset and model the hydra config that links to each script (seen above each main method). With `vllm` run with flag `-m` to submit slurm job. For `sandbox` (or any models using the Portkey API) run with `python <<file>> api_key=<<your_api_key`>>. 

Some notes:
Llama-3.3-70B requires that you run with vllm_env and 4 GPUs (make sure to change the num_gpus in both the variable and in the script at the bottom).
hydra:
  launcher:
    timeout_min: x
    mem_gb: 8
    gres: gpu:4
    setup:
      - export HYDRA_FULL_ERROR=1
      - module purge
      - module load anaconda3/2024.6
      - conda activate vllm_env

Qwen3-32B requires that you run with vllm_env and 2 GPUs.

gpt4o only requires an API key (the other configs are ignored)

gpt-oss-12b requires that you run with (conda env) gptoss and 2 GPUs. You don't need a model path.

hydra:
  launcher:
    timeout_min: 1000
    mem_gb: 120
    gres: gpu:2
    setup:
      - export HYDRA_FULL_ERROR=1
      - module purge
      - module load anaconda3/2024.6
      - conda activate gptoss

This documentation is fairly basic, so if you are running into issues, please feel free to open an issue or email the authors. Cheers!
