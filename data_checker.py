import json
import os

def main():
    for dataname in [ "CodeNet"]: # "DeprecatedCode", "SafeCoder", "CodeNet", "Defects4J", "CVEFixes"
        if dataname == "DeprecatedCode":
            lib = "pandas"
            corpus = f"corpus-{lib}.jsonl"
            qrels = f"qrels-{lib}.jsonl"
            query = f"query-{lib}.jsonl"
        
        if dataname == "CodeNet":
            corpus = f"corpus_bug.jsonl"
            query = f"query_bug.jsonl"
            qrels = f"qrels_bug.jsonl"
            
        else:
            corpus = f"corpus.jsonl"
            query = f"query.jsonl"
            qrels = f"qrels.jsonl"
        
        docids, queryids, qrelids = [], [], []
        with open(os.path.join("datasets", dataname, corpus), "r") as f:
            for idx, line in enumerate(f):
                # if idx > 10:
                #     break
                data = json.loads(line)
                for item in ["doc-id", "lang", "src", "title", "text"]:
                    if not item in data:
                        print(f"{item} not in the {idx}-th {dataname} {corpus}")
                docids.append(data["doc-id"])
                        
                        
        with open(os.path.join("datasets", dataname, query), "r") as f:
            for idx, line in enumerate(f):
                # if idx > 10:
                #     break
                data = json.loads(line)
                for item in ["query-id", "src", "title", "text"]:
                    if not item in data:
                        print(f"{item} not in the {idx}-th {dataname} {query}")
                queryids.append(data["query-id"])
                        
                        
        with open(os.path.join("datasets", dataname, qrels), "r") as f:
            for idx, line in enumerate(f):
                if idx > 20:
                    break
                data = json.loads(line)
                for item in ["qid", "pos-docids", "neg-docids", "type", "meta"]:
                    if not item in data:
                        print(f"{item} not in the {idx}-th data")
                if data["qid"] not in queryids:
                    print(f"{data['qid']} not in queryids")
                
                if len(data["pos-docids"]) == 0 :
                    print(f"{data['qid']} has no pos docids")
                    
                if len(data["neg-docids"]) == 0 :
                    print(f"{data['qid']} has no neg docids")
                    
                print(len(data["pos-docids"]), len(data["neg-docids"]))
                for posid in data["pos-docids"]:
                    if posid not in docids:
                        print(f"{posid} not in docids")
                
                for negid in data["neg-docids"]:
                    if negid not in docids:
                        print(f"{negid} not in docids")
                

if __name__ == "__main__":
    main()
    