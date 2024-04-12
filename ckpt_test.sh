
full_path="/home/wanghaoyu/MiniCPM/finetune/MiniCPM-2b-bp16-sft/fr_all/20240322222014"
python ckpt_auto_test.py \
    --gpu_id 2,3,4,5,6,7 \
    --port 6325 --model_type minicpm \
    --test_list humaneval \
    --languages fr \
    --model_path ${full_path} 
