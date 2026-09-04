# ShineMnemos Memory API (Base Mainnet x402, Paid)

Grounded memory for AI agents: answers pass the knowledge graph, facts pass a truth gate on write, provenance is read back on recall, and every pass is journaled.

## Service

- Catalog FQN: `shinemnemos`
- Category: `ai_ml`
- Chains: `eip155:8453` (Base Mainnet)
- Schemes: `exact` + USDC (EIP-3009 supported by facilitators)
- Tags: memory, mcp, grounded, x402
- Listed price: `0.0035 USD` per memory op (intro price, -30% of the 0.005 baseline); hosted plans from `19 USD/month` (annual -40%)

## How to pay

1. **Pay-per-call** — `POST https://shinegang.click/api/payg/quote` with `{"ops": N}` returns an HTTP 402 challenge: pay exactly `N x 0.0035 USDC` to the quoted `payTo` on Base, then `POST /api/payg/complete` with the tx hash. The ops land on the account balance.
2. **Plans** — `POST https://shinegang.click/api/plans/{id}/challenge` (`period: month | annual`) quotes the tier price; complete with the tx hash and the plan activates on-chain. Upgrades are prorated: pay only the price difference for the days left.

## Notes

- One transaction = one redemption (global replay guard). The payer must be the wallet that signed in.
- First 1,000 accounts: any payment strictly above 0.005 USDC unlocks Pro for 30 days, once per account.
- Open source (Apache-2.0), self-host free: https://github.com/shinegang/shinemnemos
- Contact: hello@shinegang.click
