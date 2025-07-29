from huggingface_hub import HfApi
import os
from dotenv import load_dotenv

load_dotenv()

api = HfApi(token=os.getenv("HF_TOKEN"))
api.upload_large_folder(
    folder_path="../dataset",
    repo_id="maxspiri/breakdance-pose-detection",
    repo_type="dataset",
)
