MODEL=/home/wanghaoyu/MiniCPM/finetune/output/es_all/vllm
# MODEL=$1
echo $MODEL

while true; do
     python URLs/vllm_url.py \
        --model_name  $MODEL\
        --gpuid  0,1,2,3\
        --port 6323 && break
    clear
    echo sleeping
    sleep 60
    echo sleep over
done
