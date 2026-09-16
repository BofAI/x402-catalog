# Render402 AI Video Generation API

Render402 is a first-party x402-paid API for MiniMax H3 video generation. Agents can create text-to-video, reference-image, first-and-last-frame, and audio-driven lip-sync jobs, paying the exact quoted amount in USDC on Base Mainnet.

## Service

- FQN: `render402`
- Base route provider: `render402-base`
- Service URL: `https://api.render402.xyz`
- Product site: `https://render402.xyz`
- OpenAPI: `https://api.render402.xyz/openapi.json`
- Pricing: `https://api.render402.xyz/v1/pricing`
- Capabilities: `https://api.render402.xyz/v1/capabilities`
- Category: `media`
- Chain: `eip155:8453` (Base Mainnet)
- Payment: USDC, x402 `exact` with EIP-3009
- Price range: $0.018 to $0.905 per generation, based on duration, resolution, and media usage

## CLI Quick Start

The smallest text-to-video request is one second at 480p. Use a new `Idempotency-Key` for each new generation intent:

```bash
x402-cli pay 'https://api.render402.xyz/v1/generate' \
  --method POST \
  --network eip155:8453 \
  --token USDC \
  --scheme exact \
  --max-amount 0.018 \
  --header 'Content-Type: application/json' \
  --header 'Idempotency-Key: replace-with-a-new-uuid' \
  --body '{"generation":{"mode":"text","model_id":"h3-video","duration":1,"resolution":"480p","aspect_ratio":"landscape","prompt":"A calm ocean at sunrise"}}'
```

For the standard five-second 480p discovery example, set `duration` to `5` and `--max-amount` to `0.09`.

## Endpoint

### POST /v1/generate

Creates a video generation job after payment settles.

Text-to-video requires:

- `generation.mode`: `text`
- `generation.prompt`: an English video description

Common optional fields include `model_id`, `duration`, `resolution`, `aspect_ratio`, and `seed`. Read `GET /v1/capabilities` before choosing a combination.

Reference-image, first-and-last-frame, and lip-sync modes require uploaded media asset IDs. Follow the public upload flow described in the OpenAPI document before paying for those modes.

The first unpaid request returns HTTP 402 with a standard x402 v2 `PAYMENT-REQUIRED` header. After the CLI settles the quoted USDC amount and retries the same request, Render402 returns HTTP 202 with URLs for following job status and retrieving the output.

## Integration Notes

- Pricing is dynamic and published at `GET /v1/pricing`.
- Never reuse an idempotency key for a different request body.
- Review the product Terms and Content Policy before submitting a generation.
- The public catalog entry contains no wallet keys, payment proofs, upstream credentials, or private media.
