# x402 Inspection Services

Two first-party x402-paid inspection tools for AI agents on Base Mainnet.

## Service

- Catalog FQN: `x402-inspection`
- Category: `devtools`
- Network: `eip155:8453` (Base Mainnet)
- Token: Circle USDC
- Scheme: x402 v2 `exact` + EIP-3009
- Price: `0.01 USDC` per request
- No signup or API key required
- Public docs/storefront: https://github.com/ipdoctor961051-cyber/x402-preflight

## Endpoints

### POST /v1/audit

URL: https://x402-preflight-mainnet.ipdoctor961051.workers.dev/v1/audit

Input JSON accepts a public HTTPS `url`, optional HTTP `method`, optional string headers, and optional body. The service probes the target without forwarding authentication, cookie, or payment credentials and reports whether the unpaid response exposes a usable x402 challenge.

### POST /v1/inspect

URL: https://x402-http-inspect.ipdoctor961051.workers.dev/v1/inspect

Input JSON accepts a public HTTPS `url` plus optional request fields. The result includes HTTP status, redirect/content metadata, a bounded body preview, and x402-related signals.

## Example unpaid discovery

```bash
curl -i -X POST \
  https://x402-http-inspect.ipdoctor961051.workers.dev/v1/inspect \
  -H 'content-type: application/json' \
  -d '{"url":"https://example.com","method":"GET"}'
```

A valid unpaid request returns HTTP `402 Payment Required` with an x402 v2 payment challenge for 0.01 USDC on Base Mainnet.

## Spend-aware usage

- Use Preflight when the task is specifically about x402 compatibility.
- Use HTTP Inspect for general endpoint diagnostics.
- Cache stable inspection results where appropriate.
- Each call is independently priced at 0.01 USDC.

## Safety notes

- Only public HTTPS targets are accepted.
- Obvious loopback/private/local targets are rejected before payment.
- Authentication, cookie and payment headers are stripped before probing the target.
- Product execution must succeed before settlement is requested.
