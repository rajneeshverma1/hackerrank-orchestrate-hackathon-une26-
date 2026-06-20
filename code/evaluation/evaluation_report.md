# Evaluation Report

## Metrics on sample_claims.csv

- **Total Claims Evaluated**: 20
- **evidence_standard_met Accuracy**: 80.00%
- **claim_status Accuracy**: 60.00%
- **issue_type Accuracy**: 60.00%
- **object_part Accuracy**: 80.00%
- **valid_image Accuracy**: 85.00%
- **severity Accuracy**: 50.00%

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
