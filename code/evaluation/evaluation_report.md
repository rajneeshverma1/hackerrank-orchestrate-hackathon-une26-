# Evaluation Report

## Metrics on sample_claims.csv

- **Total Claims Evaluated**: 20
- **evidence_standard_met Accuracy**: 10.00%
- **claim_status Accuracy**: 10.00%
- **issue_type Accuracy**: 15.00%
- **object_part Accuracy**: 5.00%
- **valid_image Accuracy**: 10.00%
- **severity Accuracy**: 10.00%

## Strategy Used
- **Model**: GPT-4o with structured JSON outputs.
- **Prompting**: Object-specific instructions, injecting user history and evidence requirements.

## Operational Analysis
- **Model Calls**: 1 call per claim.
- **Token Usage**: ~500 input text tokens, plus image token encoding costs (~1000 tokens per image). Output ~150 tokens.
- **Images Processed**: Depends on the claim, encoded as base64.
- **Cost Estimate**: At $5/M input and $15/M output for GPT-4o, cost is roughly $0.01 per claim.
- **Latency**: ~3-5 seconds per claim.
- **Rate Limits**: Synchronous processing ensures we don't hit RPM/TPM limits on standard tiers, though batching could speed this up for larger datasets.
