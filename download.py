from datasets import load_dataset, Split
import os

config_list = ['en', 'fr', 'pt', 'jp', 'ru', 'zh']

for config in config_list:
    try:
        dataset = load_dataset("Muennighoff/xwinograd", config)['test']
    except Exception as e:
        print(f"Failed to download {config} dataset: {e}")
        continue
    # 将数据集转换为pandas DataFrame
    df = dataset.to_pandas()
    # 保存为JSON Lines文件，禁止ASCII转义
    df.to_json(f'./RawData/xwinograd/{config}.jsonl', orient='records', lines=True, force_ascii=False)