# R2 x402 Manifest Audit API (Base Mainnet, Paid)

Deterministic static inspection of an inline x402 manifest. The service returns structured findings about payment requirement bindings and never fetches URLs supplied in the manifest.

## Service

- Catalog FQN: `r2-x402-manifest-audit`
- Gateway provider identifier: `r2-x402-manifest-audit-base`
- Category: `devtools`
- Chain: `eip155:8453` (Base Mainnet)
- Asset: canonical USDC
- Scheme: x402 v2 `exact` with EIP-3009
- Price: `$2.00 USD` per successful report
- Recipient: `0x605519164197f8464503950196BdB9a932c90Cdb`
- Source and full boundaries: https://github.com/ruizmr/x402-api-readiness-review

## Endpoint

`POST https://r2-x402-manifest-audit.dragonfly27.workers.dev/v1/check`

Request body, maximum 262144 bytes:

```json
{"manifest": {"resources": []}}
```

Probe without payment (returns HTTP 402 and a `PAYMENT-REQUIRED` header):

```bash
curl -i -X POST 'https://r2-x402-manifest-audit.dragonfly27.workers.dev/v1/check'   -H 'Accept: application/json'   -H 'Content-Type: application/json'   --data '{"manifest":{}}'
```

Use an x402 v2 client that independently caps the amount, verifies Base mainnet, canonical USDC, and the exact recipient before signing. Never paste a private key into a request or issue.

## Output

A successful paid call returns a JSON report with requirement and finding counts, severity-ranked finding objects, and explicit limitations. Malformed input returns non-2xx and the middleware does not settle it.

## Boundaries

- Static JSON inspection only.
- Does not test runtime payment enforcement or settlement.
- Does not validate signatures, replay defenses, facilitator trust, token value, contract safety, or legal compliance.
- A clean report is not a security audit or certification.
- The public facilitator is an external availability, verification, and settlement dependency.
