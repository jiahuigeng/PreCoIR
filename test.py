import json
for i in range(10):
    qrels_bug = f"datasets/CodeNet/qrels_bug_{i}.jsonl"
    # qrels_effi = f"datasets/CodeNet/qrels_effi_{i}.jsonl"
    with open(qrels_bug, "r", encoding="utf-8") as f:
        lines = f.readlines()
        data = json.loads(lines[0])
        print(len(data["pos-docids"]), len(data["neg-docids"]))
        
    # with open(qrels_effi, "r", encoding="utf-8") as f:
    #     lines = f.readlines()
    #     data = json.loads(lines[0])
    #     print(len(data["pos-docids"]), len(data["neg-docids"]))
