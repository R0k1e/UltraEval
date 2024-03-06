#!/bin/bash
#SBATCH --partition=gpu3-1
#SBATCH --nodelist=g3005
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --gres=gpu:8
#SBATCH --cpus-per-task=8

#/data/public/wangshuo/bloomz-7b1-mt
#/data/public/wangshuo/PolyLM-multialpaca-13b
#/data/public/wangshuo/polylm-chat-13b
#/data/public/opensource_models/meta-llama/Llama-2-7b-chat-hf
#/data/public/wangshuo/exp/ft-5lang-omg-13b/ckpts/checkpoints/epoch_2_hf
# /home/wanghaoyu/analyse_data/phoenix-inst-chat-7b
# /home/wanghaoyu/analyse_data/chimera-inst-chat-13b
# /home/wanghaoyu/analyse_data/guanaco-13b-hf
# /home/wanghaoyu/analyse_data/Guanaco

# MODEL=/home/wanghaoyu/UltraLink/model_weight
MODEL=$1
echo $MODEL
python URLs/transformer_url.py \
    --model_name  $MODEL\
    --gpuid  0,1\
    --port 6323

