# x402-ping (Base Mainnet x402, Paid)

Live Cloudflare Worker for free tip/unlock discovery plus a Base USDC x402 `/premium` paywall. Useful for agent payment-path checks and directory health probes.

## Service

- Catalog FQN: `x402-ping`
- Category: `devtools`
- Chains: `eip155:8453` (Base Mainnet)
- Schemes: `exact` + USDC (EIP-3009 via facilitators)
- Tags: x402, ping, base, usdc, devtools
- Listed price: `0.05 USD` per `/premium` call
- payTo: `0xbAd41cF0f0d5442f9A53630F8081BFd257DA019b`
- Asset: Base USDC `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`

## How to pay

1. **Free discovery** — `GET https://x402-ping.palmbeachpete.workers.dev/` returns treasury, tip, unlock, and network metadata (no payment).
2. **Premium ping** — `GET https://x402-ping.palmbeachpete.workers.dev/premium` answers with HTTP 402 exact `0.05 USDC` on Base. Pay via an x402 client/facilitator, then retry with the payment proof to receive pong JSON.

```bash
x402-cli pay 'https://x402-ping.palmbeachpete.workers.dev/premium' \
  --method GET \
  --network eip155:8453 \
  --token USDC \
  --scheme exact \
  --max-amount 0.05
```

## Notes

- Manifests: `/.well-known/x402` and `/.well-known/agent.json`
- Source: https://github.com/filip-study/x402-ping
- Tip: https://shieldz.cash/tip/tip-d2599a4d16a6f4b0
- Unlock: https://shieldz.cash/unlock/NDS0MgohhA3PmPaBvmD0
- Operator contact: palmbeachpete@agentmail.to
