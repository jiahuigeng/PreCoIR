from huggingface_hub import HfApi, upload_folder

# Initialize the Hugging Face API
api = HfApi()

filename = ["corpus_bug.jsonl", "query_bug.jsonl", "qrels_bug.jsonl"]
for f in filename:
    local_file_path = f"datasets/CodeNet/{f}"
    print(f"upload {f}")
    # Upload the file to a specific location
    api.upload_file(
        path_or_fileobj=local_file_path,
        path_in_repo=local_file_path,  # Destination path in the repository
        repo_id="jiahuimbzuai/precoir",  # Replace with your repo name
        repo_type="dataset"  # Use "model" for model repositories
    )
