import os
from pathlib import Path
import sys

# Add parent dir to path to import code modules
sys.path.append(str(Path(__file__).parent.parent.resolve()))

from utils import load_csv, save_csv
from pipeline import process_claim
from evaluation.metrics import calculate_accuracy, generate_report

def prepare_history(history_data):
    history_dict = {}
    for row in history_data:
        uid = row.get("user_id")
        if uid:
            summary = f"Past Claims: {row.get('past_claim_count')}. "
            summary += f"Rejected: {row.get('rejected_claim')}. "
            summary += f"Flags: {row.get('history_flags')}. "
            summary += f"Summary: {row.get('history_summary')}"
            history_dict[uid] = summary
    return history_dict

def prepare_requirements(req_data):
    req_dict = {}
    for row in req_data:
        obj = row.get("claim_object")
        applies = row.get("applies_to")
        evidence = row.get("minimum_image_evidence")
        if obj not in req_dict:
            req_dict[obj] = ""
        req_dict[obj] += f"- For {applies}: {evidence}\n"
    return req_dict

def main():
    repo_root = Path(__file__).parent.parent.parent.resolve()
    dataset_dir = repo_root / "dataset"
    
    sample_file = dataset_dir / "sample_claims.csv"
    history_file = dataset_dir / "user_history.csv"
    req_file = dataset_dir / "evidence_requirements.csv"
    output_report = repo_root / "code" / "evaluation" / "evaluation_report.md"
    
    print("Loading evaluation data...")
    sample_data = load_csv(str(sample_file))
    history_data = load_csv(str(history_file))
    req_data = load_csv(str(req_file))
    
    user_history_dict = prepare_history(history_data)
    requirements_dict = prepare_requirements(req_data)
    
    results = []
    total = len(sample_data)
    
    print(f"Evaluating {total} sample claims...")
    for idx, row in enumerate(sample_data):
        print(f"[{idx+1}/{total}] Processing sample {row['user_id']}...")
        result = process_claim(row, user_history_dict, requirements_dict, str(repo_root))
        results.append(result)
        
    print("Calculating metrics...")
    metrics = calculate_accuracy(results, sample_data)
    
    generate_report(metrics, total, str(output_report))
    print(f"Evaluation complete! Report saved to {output_report}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
