# Penny Press

Penny Press is a pseudonymous imprint for original writings on freedom, truth and
the structures around us: free for humans, paid for machines. Machine
reads are priced by piece length in USDC, settled directly to the publication
wallet over the x402 protocol — no accounts, no API keys, no platform escrow.

Use it when an agent wants original writing as reading or input
material, or when testing x402 payment flows against a live endpoint.

## Pricing tiers

- Fragments (under ~100 words): $0.01
- Ensembles (100–600 words): $0.02
- Prose/long-form (600+ words): $0.05

New pieces are published over time; all machine reads follow the tier schedule above.

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
| Untamed Wilderness | `https://www.pennypress.org/essays/untamed-wilderness` | $0.01 |
| Thermodynamic Proof | `https://www.pennypress.org/essays/thermodynamic-proof` | $0.01 |
| Techno-Feudalism at the UN: Corporate Capture and the Geopolitics of AI | `https://www.pennypress.org/essays/techno-feudalism-un` | $0.05 |
| Small Change | `https://www.pennypress.org/essays/small-change` | $0.01 |
| Pax Decentralia | `https://www.pennypress.org/essays/pax-decentralia` | $0.02 |
| Big Stakes | `https://www.pennypress.org/essays/big-stakes` | $0.01 |
| Contradictions of the Archipelago | `https://www.pennypress.org/essays/contradictions-of-the-archipelago` | $0.02 |
| The Path of Least Resistance - Freedom and Security | `https://www.pennypress.org/essays/the-path-of-least-resistance` | $0.02 |
| The Agentic Paradigm: How Artificial Intelligence Demobilizes Labour and Redefines the State | `https://www.pennypress.org/essays/the-agentic-paradigm` | $0.05 |
| Root and Cable | `https://www.pennypress.org/essays/root-and-cable` | $0.01 |
| Fabricated Frontiers | `https://www.pennypress.org/essays/fabricated-frontiers` | $0.02 |
| Essays — full set (all pieces) | `https://www.pennypress.org/essays/full` | dynamic (see 402) |

Machine-readable catalog: `https://www.pennypress.org/essays` (free).
Humans read free: `https://www.pennypress.org/read/{slug}`.
Or get every piece in one payment: `https://www.pennypress.org/essays/full` — the bundle price is set below the combined per-piece total and recomputed as the catalog grows; the 402 response always states the current price.

## Glossary

Key terms are defined by the author as used across the essays. Each
definition is delivered as JSON after a $0.01 USDC x402 payment on Base
mainnet; humans read the same definitions free at `/read/glossary/{term}`.
Browse the free term list at `https://www.pennypress.org/glossary`.
Or get all definitions in one payment: `https://www.pennypress.org/glossary/full` ($0.25).

| Term | URL | Price |
|---|---|---|
| Glossary — full set (all definitions) | `https://www.pennypress.org/glossary/full` | $0.25 |
| Denizens | `https://www.pennypress.org/glossary/denizens` | $0.01 |
| perdition | `https://www.pennypress.org/glossary/perdition` | $0.01 |
| connoisseurs | `https://www.pennypress.org/glossary/connoisseurs` | $0.01 |
| behemoths | `https://www.pennypress.org/glossary/behemoths` | $0.01 |
| poignant | `https://www.pennypress.org/glossary/poignant` | $0.01 |
| cohort | `https://www.pennypress.org/glossary/cohort` | $0.01 |
| sacrosanct | `https://www.pennypress.org/glossary/sacrosanct` | $0.01 |
| unabated | `https://www.pennypress.org/glossary/unabated` | $0.01 |
| lawfare | `https://www.pennypress.org/glossary/lawfare` | $0.01 |
| august | `https://www.pennypress.org/glossary/august` | $0.01 |
| metropoles | `https://www.pennypress.org/glossary/metropoles` | $0.01 |
| tomfoolery | `https://www.pennypress.org/glossary/tomfoolery` | $0.01 |
| crony capitalism | `https://www.pennypress.org/glossary/crony-capitalism` | $0.01 |
| hyperscalers | `https://www.pennypress.org/glossary/hyperscalers` | $0.01 |
| multilateral | `https://www.pennypress.org/glossary/multilateral` | $0.01 |
| stewardship | `https://www.pennypress.org/glossary/stewardship` | $0.01 |
| plethora | `https://www.pennypress.org/glossary/plethora` | $0.01 |
| cornucopia | `https://www.pennypress.org/glossary/cornucopia` | $0.01 |
| demonetized | `https://www.pennypress.org/glossary/demonetized` | $0.01 |
| demobilized | `https://www.pennypress.org/glossary/demobilized` | $0.01 |
| Pax Americana | `https://www.pennypress.org/glossary/pax-americana` | $0.01 |
| Pax Decentralia | `https://www.pennypress.org/glossary/pax-decentralia` | $0.01 |
| techno-feudal | `https://www.pennypress.org/glossary/techno-feudal` | $0.01 |
| material contradictions | `https://www.pennypress.org/glossary/material-contradictions` | $0.01 |
| materialism | `https://www.pennypress.org/glossary/materialism` | $0.01 |
| axioms | `https://www.pennypress.org/glossary/axioms` | $0.01 |
| macro-trajectory | `https://www.pennypress.org/glossary/macro-trajectory` | $0.01 |
| thermodynamic | `https://www.pennypress.org/glossary/thermodynamic` | $0.01 |
| Luddites | `https://www.pennypress.org/glossary/luddites` | $0.01 |
| cryptographic | `https://www.pennypress.org/glossary/cryptographic` | $0.01 |

## CLI Quick Start

Install or update the x402 CLI, then pay for the piece you want to read:

```bash
x402-cli pay 'https://www.pennypress.org/essays/thermodynamic-proof' \
  --network eip155:8453 --token USDC --scheme exact --max-amount 0.01
```

The CLI handles the 402 challenge, signs the USDC payment on Base mainnet,
and returns the piece text.
