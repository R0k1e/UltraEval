#!/bin/bash
#SBATCH --partition=gpu3-1
#SBATCH --nodelist=g3005
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --gres=gpu:8
#SBATCH --cpus-per-task=8
#/data/public/wangshuo/exp/ft-ru-alpaca-llama-2-7b/ckpts/checkpoints/epoch_2_hf
#/data/public/wangshuo/exp/ft-ru-alpaca-know-llama-2-7b/ckpts/checkpoints/epoch_2_hf
#/data/public/wangshuo/exp/zh_code_learn_dynamics/from-magicoder/epoch_2_hf
#/data/public/wangshuo/exp/zh_code_learn_dynamics/from-llama-2-7b/epoch_2_hf

#/data/public/wangshuo/exp/ft-5lang-llama-2-7b/ckpts/checkpoints/epoch_2_hf
#/data/public/wangshuo/bloomz-7b1-mt
#/data/public/wangshuo/PolyLM-multialpaca-13b
#/data/public/wangshuo/polylm-chat-13b
#/data/public/opensource_models/meta-llama/Llama-2-7b-chat-hf


MODEL=/home/wanghaoyu/mAlign-shuo-dev/ckpts/checkpoints/step_8900_hf

# MODEL=$1
echo $MODEL
python URLs/vllm_url.py \
    --model_name  $MODEL\
    --gpuid  6,7\
    --port 6325