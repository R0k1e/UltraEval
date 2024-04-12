import os
import sys
import subprocess

if __name__ == '__main__':
    ckpt_dir = "/home/wanghaoyu/MiniCPM/finetune/MiniCPM-2B-history"
    for data_type in os.listdir(ckpt_dir):
        for lr_set in os.listdir(os.path.join(ckpt_dir, data_type)):
            for exec_time in os.listdir(os.path.join(ckpt_dir, data_type, lr_set)):
                    full_path = os.path.join(ckpt_dir, data_type, lr_set, exec_time)
                    command = f"""python ckpt_auto_test.py \
                                --gpu_id 0,1,2,3,4,5,6,7 \
                                --port 6325 --model_type minicpm-raw \
                                --test_list humaneval \
                                --languages en \
                                --model_path {full_path} """
                    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
                    while True:
                        if process.poll() is not None:
                            print('End of subprocess')
                            break
                    