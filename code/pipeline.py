import os
from typing import Dict, Any
from openai import OpenAI

from utils import encode_image
from models import ClaimPrediction
from prompts import SYSTEM_PROMPT, build_user_prompt
from dotenv import load_dotenv

# Load API key
load_dotenv()

# Assuming OPENAI_API_KEY is set in environment
client = OpenAI()

def process_claim(row: Dict[str, str], user_history_dict: Dict[str, str], requirements_dict: Dict[str, str], repo_root: str) -> Dict[str, Any]:
    user_id = row['user_id']
    image_paths_raw = row['image_paths']
    user_claim = row['user_claim']
    claim_object = row['claim_object']
    
    # Get history
    history = user_history_dict.get(user_id, "No history available.")
    
    # Get requirements (simplification: get all for the object)
    reqs = requirements_dict.get(claim_object, "")
    if not reqs:
        reqs = requirements_dict.get("all", "No specific requirements.")
        
    prompt = build_user_prompt(user_claim, claim_object, reqs, history)
    
    image_paths = [p.strip() for p in image_paths_raw.split(';') if p.strip()]
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]
    
    user_content = [{"type": "text", "text": prompt}]
    
    for img_path in image_paths:
        full_path = os.path.join(repo_root, "dataset", img_path)
        base64_img = encode_image(full_path)
        if base64_img:
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_img}"
                }
            })
            
    messages.append({"role": "user", "content": user_content})
    
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=messages,
            response_format=ClaimPrediction,
            temperature=0.0
        )
        prediction = completion.choices[0].message.parsed
        
        result = {
            'user_id': user_id,
            'image_paths': image_paths_raw,
            'user_claim': user_claim,
            'claim_object': claim_object,
            'evidence_standard_met': str(prediction.evidence_standard_met).lower(),
            'evidence_standard_met_reason': prediction.evidence_standard_met_reason,
            'risk_flags': ";".join(prediction.risk_flags) if isinstance(prediction.risk_flags, list) else prediction.risk_flags,
            'issue_type': prediction.issue_type,
            'object_part': prediction.object_part,
            'claim_status': prediction.claim_status,
            'claim_status_justification': prediction.claim_status_justification,
            'supporting_image_ids': ";".join(prediction.supporting_image_ids) if isinstance(prediction.supporting_image_ids, list) else prediction.supporting_image_ids,
            'valid_image': str(prediction.valid_image).lower(),
            'severity': prediction.severity
        }
        return result
    except Exception as e:
        print(f"Error processing claim {user_id}: {e}")
        # Fallback empty result
        return {
            'user_id': user_id,
            'image_paths': image_paths_raw,
            'user_claim': user_claim,
            'claim_object': claim_object,
            'evidence_standard_met': 'false',
            'evidence_standard_met_reason': f'Error: {e}',
            'risk_flags': 'none',
            'issue_type': 'unknown',
            'object_part': 'unknown',
            'claim_status': 'not_enough_information',
            'claim_status_justification': 'Processing failed',
            'supporting_image_ids': 'none',
            'valid_image': 'false',
            'severity': 'unknown'
        }
