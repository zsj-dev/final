import json
from collections import defaultdict

# 存储每个task_id的计数器
task_id_counts = defaultdict(int)

# 存储每个task_id的前5个JSON对象
task_id_objects = defaultdict(list)

# 遍历所有文件
with open('output_prompt_1.jsonl', 'r') as f:
    # 逐行读取文件内容
    for line in f:
        # 解析JSON对象
        json_obj = json.loads(line.strip())
        task_id = json_obj['task_id']
        
        # 如果该task_id的计数器小于5，则将该JSON对象添加到列表中
        if task_id_counts[task_id] < 5:
            task_id_objects[task_id].append(json_obj)
            task_id_counts[task_id] += 1

# 将结果写入新文件
with open('output_1_5.jsonl', 'w') as f:
    for task_id, objects in task_id_objects.items():
        for obj in objects:
            f.write(json.dumps(obj) + '\n')