# Nonsynthetic — Apex Edge (Base Mainnet x402, Paid)

Agent-native commerce node: 298 machine-payable routes over x402 v2 — security audits, treasury forensics, corpus search, utility APIs. First-party service, no gateway intermediary.

## Service

- Catalog FQN: `nonsynthetic`
- Category: `security`
- Chains: `eip155:8453` (Base Mainnet) — Solana `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` also accepted via PayAI facilitator
- Scheme: `exact` + USDC EIP-3009 `transferWithAuthorization`
- PayTo: `0xe70F099F0e139f8A2D8ac6E48f7457d99738B968` (Base)
- Machine catalog: `https://api.nonsynthetic.net/.well-known/x402` (298 products, 260 resources)
- Agent card: `https://api.nonsynthetic.net/.well-known/agent-card.json` (A2A v0.3.0, JWS-signed)
- Listed price range: `$0.002` – `$20` per call

## When To Use

- Deterministic security gates: audit checklist ($0.05), LLM audit verdict ($0.25), address risk screen ($0.02)
- Treasury reconciliation: forensic ERC-20 census ($20) or bounded scan ($2) — both Ed25519-signed
- Corpus research over 496 indexed documents ($0.01/call)
- MCP-native clients: `POST /mcp` with per-tool pricing

## How To Pay

1. Call any paid route → HTTP 402 returns `accepts[]` (x402 v2, `scheme: exact`, USDC atomic units on `eip155:8453`).
2. Settle via Coinbase CDP facilitator or PayAI facilitator — the challenge carries `facilitator` hints per network.
3. Replay the request with the x402 payment payload. Settled calls return a public receipt (`/api/v1/receipts/{hash}`).

Free evaluation: select utility routes allow 5 calls/day/IP before 402 — enough to verify output shape before spending.

## Provenance

- ERC-8004 agent id `1179000` (`eip155:8453`)
- settled.tools seller record: https://settled.tools/s/0xe70f099f0e139f8a2d8ac6e48f7457d99738b968
- Start guide: https://api.nonsynthetic.net/start.html
