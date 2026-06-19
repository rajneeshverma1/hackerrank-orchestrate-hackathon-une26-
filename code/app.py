import streamlit as st
import os
import base64
from pathlib import Path

# Fix imports since this is run as a script
import sys
sys.path.append(str(Path(__file__).parent.parent.resolve()))

from code.pipeline import process_claim
from code.utils import load_csv

def main():
    st.set_page_config(page_title="Evidence Review UI", layout="wide")
    st.title("🛡️ HackerRank Orchestrate: Damage Claim Verification")
    
    st.markdown("Test the evidence review system locally!")
    
    repo_root = Path(__file__).parent.parent.resolve()
    
    # Simple form
    with st.sidebar:
        st.header("Claim Details")
        user_id = st.text_input("User ID", value="user_001")
        claim_object = st.selectbox("Claim Object", ["car", "laptop", "package"])
        user_claim = st.text_area("User Claim Transcript", "I dropped my laptop and the screen cracked.")
        
        uploaded_file = st.file_uploader("Upload Damage Image", type=["jpg", "jpeg", "png"])
        
        verify_btn = st.button("Verify Claim", type="primary")

    if verify_btn:
        if not uploaded_file:
            st.warning("Please upload an image first.")
            return
            
        # Save uploaded file temporarily
        temp_dir = repo_root / "dataset" / "temp_uploads"
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_path = temp_dir / uploaded_file.name
        
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        # Prepare mock history and requirements dicts for testing
        history_dict = {user_id: "Past Claims: 0. Clean history."}
        req_dict = {claim_object: f"- For {claim_object}: Needs clear photo of damage."}
        
        row = {
            'user_id': user_id,
            'image_paths': f"temp_uploads/{uploaded_file.name}",
            'user_claim': user_claim,
            'claim_object': claim_object
        }
        
        st.info("Analyzing claim with VLM...")
        
        # Display the image
        st.image(uploaded_file, caption="Uploaded Evidence", width=400)
        
        result = process_claim(row, history_dict, req_dict, str(repo_root))
        
        st.success("Analysis Complete!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Evidence Standard Met", result['evidence_standard_met'])
            st.write(f"**Reason:** {result['evidence_standard_met_reason']}")
            
            st.metric("Claim Status", result['claim_status'].upper())
            st.write(f"**Justification:** {result['claim_status_justification']}")
            
        with col2:
            st.write(f"**Issue Type:** {result['issue_type']}")
            st.write(f"**Object Part:** {result['object_part']}")
            st.write(f"**Risk Flags:** {result['risk_flags']}")
            st.write(f"**Severity:** {result['severity']}")
            
        st.json(result)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
