from pathlib import Path

from utils import load_csv, save_csv
from pipeline import process_claim

def prepare_history(history_data):
    # Returns a dictionary: user_id -> string summary
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
    # Returns a dictionary: claim_object -> requirements string
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
    repo_root = Path(__file__).parent.parent.resolve()
    dataset_dir = repo_root / "dataset"
    
    claims_file = dataset_dir / "claims.csv"
    history_file = dataset_dir / "user_history.csv"
    req_file = dataset_dir / "evidence_requirements.csv"
    output_file = repo_root / "output.csv"
    
    print("Loading data...")
    claims_data = load_csv(str(claims_file))
    history_data = load_csv(str(history_file))
    req_data = load_csv(str(req_file))
    
    user_history_dict = prepare_history(history_data)
    requirements_dict = prepare_requirements(req_data)
    
    results = []
    total = len(claims_data)
    import time
    
    existing_results = {}
    if output_file.exists():
        try:
            old_data = load_csv(str(output_file))
            for old_row in old_data:
                uid = old_row.get("user_id")
                reason = old_row.get("evidence_standard_met_reason", "")
                justification = old_row.get("claim_status_justification", "")
                if uid and "Error" not in reason and "Processing failed" not in justification:
                    existing_results[uid] = old_row
            print(f"Found {len(existing_results)} valid existing predictions in output.csv. Resuming...")
        except Exception as e:
            print(f"Could not load output.csv for resuming: {e}")

    print(f"Processing {total} claims...")
    for idx, row in enumerate(claims_data):
        uid = row['user_id']
        if uid in existing_results:
            print(f"[{idx+1}/{total}] Skipping user {uid} (already successfully processed)...")
            results.append(existing_results[uid])
            continue
            
        print(f"[{idx+1}/{total}] Processing user {uid}...")
        result = process_claim(row, user_history_dict, requirements_dict, str(repo_root))
        results.append(result)
        if idx < total - 1:
            time.sleep(1.5)


        
    fieldnames = [
        "user_id", "image_paths", "user_claim", "claim_object",
        "evidence_standard_met", "evidence_standard_met_reason",
        "risk_flags", "issue_type", "object_part", "claim_status",
        "claim_status_justification", "supporting_image_ids",
        "valid_image", "severity"
    ]
    
    save_csv(str(output_file), fieldnames, results)
    print(f"Done! Results saved to {output_file}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
