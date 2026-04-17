Download oral-args-data-set and store all the automated metrics into a folder data/

Run any main. With `vllm` run with flag `-m` to submit slurm job. For `sandbox` run with `python <<file>> api_key=<<your_api_key`>>

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