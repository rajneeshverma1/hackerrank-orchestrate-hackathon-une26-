# Evaluation Report: Operational Analysis

## Usage & Scale Metrics
- **Approximate number of model calls:** ~50 model calls (44 claims in the test dataset `claims.csv` and 5 in the sample dataset `sample_claims.csv`).
- **Number of images processed:** ~55-60 images (some claims contain multiple images).
- **Approximate input/output token usage:** 
  - **Input:** ~1,600 tokens per call (~500 text tokens for the prompt, ~1,100 tokens for the base64-encoded image). Total: ~80,000 input tokens.
  - **Output:** ~100 tokens per call (for the structured JSON response). Total: ~5,000 output tokens.

## Cost & Latency
- **Approximate cost:** Using Groq's high-speed Llama 4 Vision models (e.g. `meta-llama/llama-4-scout-17b-16e-instruct`), the pricing is roughly $0.11 per 1M input tokens and $0.34 per 1M output tokens. 
  - Input Cost: $0.0088
  - Output Cost: $0.0017
  - **Total Cost:** ~$0.01 for the entire test set.
- **Approximate latency/runtime:** ~1.5 to 2 seconds per claim on Groq. Total sequential runtime for the full 44-row test set is roughly **60 to 90 seconds**.

## Engineering Considerations (TPM/RPM & Strategies)
- **Rate Limiting & Concurrency:** The current pipeline implements sequential processing. While batching or concurrent async requests (`asyncio.gather`) would reduce total runtime to <5 seconds, sequential processing was chosen to strictly respect Groq's aggressive Requests-Per-Minute (RPM) free-tier rate limits and avoid HTTP 429 errors.
- **Production Enhancements:**
  - **Caching:** In a production setting, hashing the image and storing the resulting LLM JSON output in a Redis cache would prevent redundant API calls for duplicate image uploads.
  - **Retries:** We rely on basic try/except blocks. A production implementation would use a library like `tenacity` for exponential backoff retries when encountering transient network or API limit errors.
  - **Batching:** If enterprise rate limits are available, we would process claims in batches of 5-10 using semaphores to maximize throughput.
