# Penny Press

Penny Press is a pseudonymous imprint for original writings on freedom, truth and
the structures around us: free for humans, paid for machines. Machine
reads are priced by piece length in USDC, settled directly to the publication
wallet over the x402 protocol — no accounts, no API keys, no platform escrow.

Use it when an agent wants original writing as reading or input
material, or when testing x402 payment flows against a live endpoint.

## Pricing tiers

- Fragments (under 100 words): $0.01
- Ensembles (short essays and briefs): $0.02
- Prose/long-form: $0.05

Four fragments ($0.01) and one long-form prose essay ($0.05) are live;
no ensembles are published yet.

## Service

- FQN: `penny-press`
- Service URL: `https://www.pennypress.org`
- Category: `media`
- Payment chain: `eip155:8453` (Base mainnet)
- Scheme: `exact` + USDC (EIP-3009 transfer)
- Settlement: direct to the publication wallet named in each 402 challenge

Penny Press settles on Base mainnet (USDC) — verified live with real payments.

## Endpoints

All endpoints are `GET` with no request body. The first call returns
`402 Payment Required` with the payment terms; pay per the x402 flow and retry
with the payment proof to receive the piece as Markdown.

| Piece | URL | Price |
|---|---|---|
| The River of Time | `https://www.pennypress.org/essays/river-of-time` | $0.01 |
| An Untamed Wilderness | `https://www.pennypress.org/essays/untamed-wilderness` | $0.01 |
| Thermodynamic Proof | `https://www.pennypress.org/essays/thermodynamic-proof` | $0.01 |
| Techno-Feudalism at the UN: Corporate Capture and the Geopolitics of AI | `https://www.pennypress.org/essays/techno-feudalism-un` | $0.05 |
| Small Change | `https://www.pennypress.org/essays/small-change` | $0.01 |

Machine-readable catalog: `https://www.pennypress.org/essays` (free).
Humans read free: `https://www.pennypress.org/read/{slug}`.

## CLI Quick Start

Install or update the x402 CLI, then pay for the piece you want to read:

```bash
x402-cli pay 'https://www.pennypress.org/essays/thermodynamic-proof' \
  --network eip155:8453 --token USDC --scheme exact --max-amount 0.01
```

The CLI handles the 402 challenge, signs the USDC payment on Base mainnet,
and returns the piece text.
