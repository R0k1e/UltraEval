#!/bin/bash

# hyperparameters
HF_MODEL_NAME=/home/wanghaoyu/MiniCPM/finetune/output/es_all/vllm  # huggingface上的模型名
PORT=8000  # gunicorn 端口号
URL="http://127.0.0.1:${PORT}/infer"  # URLs/gunicorn_conf.py 修改端口号
# NUMBER_OF_THREAD=1  # 线程数，一般设为 gpu数/per-proc-gpus
# CONFIG_PATH=configs/eval_config.json  # 评测文件路径[]
# OUTPUT_BASE_PATH=result/${TASK_NAME}/${MODEL_NAME}   # 结果保存路径，与HF_MODEL_NAME一致



# 步骤2
# 启动 gunicorn 并保存 PID
bash URLs/start_gunicorn.sh --hf-model-name $HF_MODEL_NAME --per-proc-gpus 2 --port $PORT& 
echo $! > gunicorn.pid


# 步骤3
# 检查服务是否已启动
MAX_RETRIES=600  # 最大尝试次数，相当于等待30分钟
COUNTER=0

while [ $COUNTER -lt $MAX_RETRIES ]; do
    sleep 30
    curl -s $URL > /dev/null
    if [ $? -eq 0 ]; then
        echo "Service is up!"
        break
    fi
    COUNTER=$((COUNTER+1))
    if [ $COUNTER -eq $MAX_RETRIES ]; then
        echo "Service did not start in time. Exiting."
        exit 1
    fi
done


# # 步骤5
# # 结束 gunicorn 进程及其 worker 进程
# MAIN_PID=$(cat gunicorn.pid)
# pgrep -P $MAIN_PID | xargs kill -9
# kill -9 $MAIN_PID
# rm gunicorn.pid