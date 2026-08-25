# GPT-5.6 Luna Standard — Base USDC x402

OpenAI-compatible GPT-5.6 Luna Standard chat for concise answers, routing decisions, extraction helpers, and buyer-owned agent trials.

## Service

- Catalog FQN: `gpt55-standard`
- Service hub: `https://gpt55.558686.xyz/x402/service`
- Endpoint: `POST https://gpt55.558686.xyz/v1/chat/completions/standard`
- Network: `eip155:8453` (Base Mainnet)
- Asset: official USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`)
- Listed price: `$0.00293` per request
- Scheme: x402 `exact` with EIP-3009

## Request

Send an OpenAI-compatible JSON body. The live HTTP 402 challenge is authoritative for the payment payload and timeout.

```json
{
  "model": "gpt-5.6-luna",
  "messages": [
    {"role": "user", "content": "Return exactly OK."}
  ],
  "max_tokens": 16
}
```

## Buyer flow

1. Open the service hub to inspect the current quote and browser-wallet checkout: `https://gpt55.558686.xyz/x402/service?checkout=standard-chat`.
2. Request the endpoint without a payment header and read the x402 `Payment-Required` challenge.
3. Sign the exact Base USDC payment with a buyer-owned wallet and retry using `Payment-Signature`.
4. Keep the HTTP 200 response and receipt metadata as delivery evidence.

For a machine-readable buyer fallback, use `https://gpt55.558686.xyz/x402/first-payment-client.mjs`.

## Compatibility

No API key, account, subscription, or platform balance is required. The service is self-hosted; the catalog entry contains public discovery metadata only.
