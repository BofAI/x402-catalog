# DefiLlama Yields / APY API (TRON x402)

x402 passthrough for DefiLlama key-free yield data: APY across thousands of DeFi pools, plus per-pool historical APY/TVL. Yield-discovery and allocation data layer for agents. Data by DefiLlama.

## Service

- FQN: `defillama-yields-tron`
- Gateway base: `https://tm-x402-gateway.bankofai.io/providers/defillama-yields-tron`
- Category: `finance`
- Chain: `tron:mainnet` (TRON)
- Scheme: `exact_gasfree`
- Tags: defillama, yield, apy, defi, pools, free
- Listed price: free (`0 USD` min and max price)

## When To Use

Use to discover and compare DeFi yields: list all pools with current APY/TVL, or pull one pool's historical APY/TVL series for allocation decisions.

## Endpoint Summary

### GET /pools

All yield pools with current APY, TVL, chain, project and risk flags
### GET /chart/{pool}

Historical APY / TVL time series for a single pool id

## Request Examples

- `GET /providers/defillama-yields-tron/pools`
- `GET /providers/defillama-yields-tron/chart/{pool_id}`

## Response Shape

- Returns DefiLlama JSON: { data: [ { pool, chain, project, symbol, tvlUsd, apy, apyBase, apyReward, stablecoin } ] }.

## Code Usage

Call the catalog route with any HTTP client. Example:

```bash
curl -sS 'https://tm-x402-gateway.bankofai.io/providers/defillama-yields-tron/pools'
```

Equivalent route form:

```text
GET https://tm-x402-gateway.bankofai.io/providers/defillama-yields-tron/pools
```

## Spend-Aware Usage

- The /pools dump is large — fetch once, then filter/cache client-side rather than re-polling each time.
- Use /chart/{pool} only for pools you actually shortlisted.

## When Not To Use

- Do not use for spot token prices (use the DefiLlama price provider) or protocol TVL alone (use the TVL provider).

## Integration Notes

- Cache responses according to the upstream data freshness needs.
- Prefer specific token, pair, protocol, pool, or address routes over broad dump/search routes when possible.
- Treat market, yield, and security data as decision support, not as the only execution signal.
- The public catalog entry only documents public routes and does not include runtime configuration or wallet material.
