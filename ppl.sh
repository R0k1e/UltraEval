TASK_NAME=arc-c
python configs/make_config.py --datasets $TASK_NAME --method ppl

python main.py \
    --model general\
    --model_args url=http://127.0.0.1:6323/vllm-url-infer,concurrency=1\
    --config_path configs/eval_config.json\
    --output_base_path logs\
    --batch_size 1024\
    --postprocess general_torch_ppl \
    --params models/model_params/vllm_logprobs.json \
    --write_out \
    