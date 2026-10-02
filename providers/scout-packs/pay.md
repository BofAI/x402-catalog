# Scout Packs — call & payment instructions (for agents and humans)

**Service:** Scout Packs by Tiger Operations
**What:** verified B2B lead packs sold per pack. No subscription, no account, no API key.
**Settlement:** USDC on Base mainnet (eip155:8453) via x402 exact.

## Packs and prices

- 25 leads — $9 USDC — instant JSON download after payment
- 50 leads — $15 USDC — assembled and delivered within 24h
- 100 leads — $25 USDC — assembled and delivered within 24h

Every lead: company name, contact name, title, published business email, source URL. Machine-readable JSON. If an email is not published, it is not in the pack.

## How to buy (agent flow)

1. Inspect payment terms — make an unpaid request; you get HTTP 402:
   curl -s -i https://scoutpacks-tunnel-1.loca.lt/packs/25
2. Pay — sign a USDC transfer on Base to the payTo address for the exact maxAmountRequired, then retry with the X-Payment header (standard x402 flow).
3. Receive — the 25-pack returns as JSON immediately. For the 50/100-pack, POST the transaction hash to /fulfill; delivered within 24h of payment confirmation.

## Discovery (machine-readable)

- Catalog: GET https://scoutpacks-tunnel-1.loca.lt/catalog (free)
- x402 manifest: GET https://scoutpacks-tunnel-1.loca.lt/.well-known/x402 (free)
- Agent notes: GET https://scoutpacks-tunnel-1.loca.lt/llms.txt (free)
- Redacted preview: GET https://scoutpacks-tunnel-1.loca.lt/packs/25/preview (free)

## Operator

Tiger Operations. Source: https://github.com/tigerops-win/scout-packs
