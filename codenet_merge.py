import os
typ = "bug"
# 目标文件
corpus_output_file = f"datasets/CodeNet/corpus_{typ}.jsonl"
query_output_file = f"datasets/CodeNet/query_{typ}.jsonl"
qrels_output_file = f"datasets/CodeNet/qrels_{typ}.jsonl"
# 确保目标文件为空
with open(corpus_output_file, "w") as f:
    pass
with open(query_output_file, "w") as f:
    pass
with open(qrels_output_file, "w") as f:
    pass

# 遍历 0 到 4052
for i in range(4053):
    input_c_file = f"datasets/CodeNet/corpus_{typ}_{i}.jsonl"
    input_q_file = f"datasets/CodeNet/query_{typ}_{i}.jsonl"
    input_r_file = f"datasets/CodeNet/qrels_{typ}_{i}.jsonl"
    
    # 检查文件是否存在
    if os.path.exists(input_c_file) and os.path.exists(input_q_file) and os.path.exists(input_r_file):
        print(i)
        with open(input_c_file, "r", encoding="utf-8") as infile, open(corpus_output_file, "a", encoding="utf-8") as outfile:
            for line in infile:
                outfile.write(line)
        
        with open(input_q_file, "r", encoding="utf-8") as infile, open(query_output_file, "a", encoding="utf-8") as outfile:
            for line in infile:
                outfile.write(line)
                
        with open(input_r_file, "r", encoding="utf-8") as infile, open(qrels_output_file, "a", encoding="utf-8") as outfile:
            for line in infile:
                outfile.write(line)
print(f"合并完成，结果保存在 {corpus_output_file}")
