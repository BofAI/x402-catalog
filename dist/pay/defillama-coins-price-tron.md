# DefiLlama Token Price API (current / historical / chart) (TRON x402)

x402 passthrough for DefiLlama key-free token prices: current, historical, charts and % change across chains by contract address. Manipulation-resistant cross-check price source for agents. Data by DefiLlama.

## Service

- FQN: `defillama-coins-price-tron`
- Gateway base: `https://tm-x402-gateway.bankofai.io/providers/defillama-coins-price-tron`
- Category: `finance`
- Chain: `tron:mainnet` (TRON)
- Scheme: `exact_gasfree`
- Tags: defillama, price, oracle, historical, multichain, free
- Listed price: free (`0 USD` min and max price)

## When To Use

Use to get current or historical USD price for one or many tokens by {chain}:{address} (or coingecko:{id}), plus price charts and percent change.

## Endpoint Summary

### GET /prices/current/{coins}

Current USD price for one or many coins ({chain}:{address} or coingecko:{id}, comma-separated)
### GET /prices/historical/{timestamp}/{coins}

Historical USD price at a unix timestamp for one or many coins
### GET /chart/{coins}

Price chart (time series) for one or many coins
### GET /percentage/{coins}

Percentage price change over a period for one or many coins

## Request Examples

- `GET /providers/defillama-coins-price-tron/prices/current/coingecko:bitcoin,coingecko:ethereum`
- `GET /providers/defillama-coins-price-tron/prices/historical/1700000000/coingecko:bitcoin`
- `GET /providers/defillama-coins-price-tron/percentage/coingecko:bitcoin`

## Response Shape

- Returns DefiLlama JSON: { coins: { 'coingecko:bitcoin': { price, symbol, timestamp, confidence } } }.

## Code Usage

Call the catalog route with any HTTP client. Example:

```bash
curl -sS 'https://tm-x402-gateway.bankofai.io/providers/defillama-coins-price-tron/prices/current/coingecko:bitcoin,coingecko:ethereum'
```

Equivalent route form:

```text
GET https://tm-x402-gateway.bankofai.io/providers/defillama-coins-price-tron/prices/current/coingecko:bitcoin,coingecko:ethereum
```

## Spend-Aware Usage

- Batch many coins in ONE call: /prices/current/ethereum:0x..,tron:T.. — one paid request returns all of them.
- Cache results; prices update on a seconds-to-minutes cadence, not per tick.

## When Not To Use

- Do not use for DEX-pair liquidity / new-launch screening (use a DEX data provider).
- Do not use for protocol TVL / fees (use the DefiLlama TVL provider).

## Integration Notes

- Cache responses according to the upstream data freshness needs.
- Prefer specific token, pair, protocol, pool, or address routes over broad dump/search routes when possible.
- Treat market, yield, and security data as decision support, not as the only execution signal.
- The public catalog entry only documents public routes and does not include runtime configuration or wallet material.
