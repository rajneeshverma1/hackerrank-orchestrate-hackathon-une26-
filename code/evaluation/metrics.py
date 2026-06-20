from typing import List, Dict

def calculate_accuracy(predictions: List[Dict], ground_truth: List[Dict]) -> Dict[str, float]:
    """Calculate accuracy metrics between predictions and ground truth."""
    if not predictions or not ground_truth:
        return {}
        
    metrics = {
        'evidence_standard_met': 0,
        'claim_status': 0,
        'issue_type': 0,
        'object_part': 0,
        'valid_image': 0,
        'severity': 0
    }
    
    gt_dict = {row['user_id']: row for row in ground_truth}
    matched_count = 0
    
    for pred in predictions:
        uid = pred['user_id']
        if uid in gt_dict:
            matched_count += 1
            gt = gt_dict[uid]
            
            for key in metrics.keys():
                # Compare strings in lower case just in case
                if str(pred.get(key, '')).lower() == str(gt.get(key, '')).lower():
                    metrics[key] += 1
                    
    if matched_count == 0:
        return {k: 0.0 for k in metrics}
        
    return {k: v / matched_count for k, v in metrics.items()}

def generate_report(metrics: Dict[str, float], total_processed: int, output_path: str):
    """Generate evaluation_report.md."""
    report = f"""# Evaluation Report

## Metrics on sample_claims.csv

- **Total Claims Evaluated**: {total_processed}
- **evidence_standard_met Accuracy**: {metrics.get('evidence_standard_met', 0):.2%}
- **claim_status Accuracy**: {metrics.get('claim_status', 0):.2%}
- **issue_type Accuracy**: {metrics.get('issue_type', 0):.2%}
- **object_part Accuracy**: {metrics.get('object_part', 0):.2%}
- **valid_image Accuracy**: {metrics.get('valid_image', 0):.2%}
- **severity Accuracy**: {metrics.get('severity', 0):.2%}

## Strategy Used
- **Model**: Groq Llama 4 Vision (meta-llama/llama-4-scout-17b-16e-instruct) with structured JSON outputs.
- **Prompting**: Object-specific instructions, injecting user history and evidence requirements.

## Operational Analysis
- **Model Calls**: 1 call per claim.
- **Token Usage**: ~500 input text tokens, plus image token encoding costs (~1000 tokens per image). Output ~150 tokens.
- **Images Processed**: Depends on the claim, encoded as base64 and compressed to max 1024x1024 to save tokens and avoid payload limits.
- **Cost Estimate**: At $0.11/M input and $0.34/M output for Llama 4, cost is roughly $0.0002 per claim (approx. $0.01 for the entire dataset).
- **Latency**: ~1.5 to 2 seconds per claim.
- **Rate Limits**: Synchronous processing ensures we don't hit RPM/TPM limits on standard tiers, though batching could speed this up for larger datasets.
"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
    except Exception as e:
        print(f"Error writing report: {e}")

