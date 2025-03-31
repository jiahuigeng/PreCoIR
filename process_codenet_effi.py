import os
import pandas as pd
import json
data_folder = "../Project_CodeNet/data"
metadata_folder = "../Project_CodeNet/metadata"
description_folder = "../Project_CodeNet/problem_descriptions"



save_folder = "datasets/CodeNet"
# save_corpus_file= os.path.join(save_folder, "corpus_effi.jsonl")
# save_query_file = os.path.join(save_folder, "query_effi.jsonl")
# save_qrels_file = os.path.join(save_folder, "qrels_effi.jsonl")

BUG = "BUG"
EFF = "EFFICIENCY"
langs = {
    "Python": "python",
    "Java": "java",
    "C++": "cpp",
    "C": "c",
    "JavaScript": "javascript",
    "Go": "go",
    "Ruby": "ruby",
    "Rust": "rust",
    "Swift": "swift",
    "TypeScript": "typescript",
}

bugs = ["Compile Error", "Wrong Answer", "Time Limit Exceeded", "Memory Limit Exceeded", "Runtime Error", "WA: Presentation Error", "Output Limit Exceeded"]
def check_contains(ss, tgt_ll):
    if any(sub in ss for sub in tgt_ll):
        return True
    return False

def search_by_id_csv(df, submission_id):
    submission_id = str(submission_id)  # Ensure it's a string
    result = df[df["submission_id"].astype(str) == submission_id]
    if not result.empty:
        return result.iloc[0].to_dict()
    else:
        return None
    
def calculate_ration(df, lang, thres=0.50):
    
    df = df[df["language"]==lang]
    cpu_time_median = df["cpu_time"].quantile(thres)#.median()
    memory_median = df["memory"].quantile(thres)#.median()
    
    return cpu_time_median, memory_median

    # # Count rows where both cpu_time and memory are below their respective medians
    # filtered_count_small = df[(df["cpu_time"] < cpu_time_median) | (df["memory"] < memory_median)].shape[0]
    # filtered_count_big = df[(df["cpu_time"] > cpu_time_median) & (df["memory"] > memory_median)].shape[0]
    # # Compute total rows
    # total_count = df.shape[0]

    # # Compute proportion
    # proportion = filtered_count_small / total_count, filtered_count_big / total_count

    
def main():
    
    
    probs = sorted(list(os.listdir(data_folder)))
    for idx, prob in enumerate(probs):
        p_corpus, p_query, p_qrels = [], [], []
        save_corpus_file, save_query_file, save_qrels_file = os.path.join(save_folder, f"corpus_effi_{idx}.jsonl"), os.path.join(save_folder, f"query_effi_{idx}.jsonl"), os.path.join(save_folder, f"qrels_effi_{idx}.jsonl")

        print(idx)
        if os.path.exists(save_corpus_file):
            continue
        metadata_csv = os.path.join(metadata_folder, f"{prob}.csv")
        metadata = pd.read_csv(metadata_csv)
        
        metadata_effi = dict()
        for lang in langs:
            if lang not in metadata_effi:
                metadata_effi[lang] = dict()
                metadata_effi[lang]["cpu_time"], metadata_effi[lang]["memory"] = calculate_ration(metadata, lang) 
            
        pos_docids, neg_docids = [], []
        
        for lang in langs:
            lang_folder = os.path.join(data_folder, prob, lang)
            if os.path.exists(lang_folder):
                pos_id, neg_id = 0, 0
                for submission in os.listdir(lang_folder):
                    submission_id = submission.split(".")[0]
                    submission_data = search_by_id_csv(metadata, submission_id)
                    if submission_data: 
                        if submission_data["status"] == "Accepted":
                            if submission_data["cpu_time"] <= metadata_effi[lang]["cpu_time"] and submission_data["memory"] <= metadata_effi[lang]["memory"]:
                                p_corpus.append({
                                    "doc-id": f"codenet-effi-{prob}-{langs[lang]}-pos{pos_id}",
                                    "lang": langs[lang],
                                    "src": "codenet",
                                    "title": "",
                                    "text": open(os.path.join(lang_folder, submission)).read(),
                                    "meta": {"submission_id": submission_id, "status": submission_data["status"], "cpu_time": submission_data["cpu_time"], "memory": submission_data["memory"]}
                                })
                                
                                pos_docids.append(f"codenet-effi-{prob}-{langs[lang]}-pos{pos_id}")
                                pos_id += 1
                            
                            elif submission_data["cpu_time"] > metadata_effi[lang]["cpu_time"] and submission_data["memory"] > metadata_effi[lang]["memory"]:
                                p_corpus.append({
                                    "doc-id": f"codenet-effi-{prob}-{langs[lang]}-neg{neg_id}",
                                    "lang": langs[lang],
                                    "src": "codenet",
                                    "title": "",
                                    "text": open(os.path.join(lang_folder, submission)).read(),
                                    "meta": {"submission_id": submission_id, "status": submission_data["status"], "cpu_time": submission_data["cpu_time"], "memory": submission_data["memory"]}
                                })
                                
                                neg_docids.append(f"codenet-effi-{prob}-{langs[lang]}-neg{neg_id}")
                                neg_id += 1

                            
        query = open(os.path.join(description_folder, f"{prob}.html")).read()
        p_query.append({
            "query-id": f"codenet-effi-{prob}",
            "src": "codenet",
            "title": "",
            "text": query,
        })
        print(f"len pos {len(pos_docids)} len neg {len(neg_docids)}")
        p_qrels.append({
            "qid": f"codenet-effi-{prob}",
            "pos-docids": pos_docids,
            "neg-docids": neg_docids,
            "type": EFF,
            "meta": "",
        })
        
        print(f"len {len(p_corpus)} {save_corpus_file}")
        with open(save_corpus_file, "w") as f:
            for doc in p_corpus:
                f.write(json.dumps(doc) + "\n")
                
        print(f"len {len(p_query)} {save_query_file}")
        with open(save_query_file, "w") as f:
            for doc in p_query:
                f.write(json.dumps(doc) + "\n")
                
        print(f"len {len(p_qrels)} {save_qrels_file}")
        with open(save_qrels_file, "w") as f:
            for doc in p_qrels:
                f.write(json.dumps(doc) + "\n")
        

                        



if __name__ == "__main__":
    main()
    
    