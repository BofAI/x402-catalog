# DefiLlama DeFi Data API (TRON, BSC and Base Mainnet x402, Paid)

x402-paid passthrough for DefiLlama protocol TVL and metadata. Paid DeFi decision data layer for agents. Data by DefiLlama.

## Service

- Catalog FQN: `defillama`
- Gateway providers: `defillama-tvl-tron`, `defillama-tvl-bsc`, `defillama-tvl-base`, `defillama-coins-price-base`, `defillama-yields-base`
- Category: `finance`
- Chains: `tron:728126428` (TRON), `eip155:56` (BNB Smart Chain), `eip155:8453` (Base Mainnet)
- Schemes: TRON/BSC `exact` + Permit2; TRON also supports `exact_gasfree`; Base Mainnet uses `exact` + USDC EIP-3009
- Tags: defillama, defi, tvl, prices, yields
- Listed price: `0.000001 USD` per request

## When To Use

Use to read protocol TVL and metadata for DeFi research, allocation or risk screening.

## Endpoint Summary

### GET /protocols

All protocols with current TVL, category and chain breakdown
### GET /protocol/{slug}

Single protocol: historical TVL, tokens and metadata
### GET /tvl/{protocol}

Current total TVL of a protocol (lightweight)

### Prices and yields

The catalog also publishes current/historical prices, price charts, percentage changes, yield pools, and pool-history endpoints. Use the matching `x402Routes` entry in the machine-readable pay JSON for the selected chain.

## Request Examples

- `GET /providers/defillama-tvl-tron/protocols`
- `GET /providers/defillama-tvl-tron/protocol/sunswap-v3`
- `GET /providers/defillama-tvl-tron/tvl/sunswap-v3`

## Response Shape

- Returns DefiLlama JSON: protocol list with tvl/chainTvls/category, or a single protocol's historical TVL and metadata.

## Code Usage

Call the catalog route with any HTTP client. Example:

```bash
curl -sS 'https://x402-gateway.bankofai.io/providers/defillama-tvl-tron/protocols'
```

Pay with the default TRON Permit2 scheme:

```bash
x402-cli pay 'https://x402-gateway.bankofai.io/providers/defillama-tvl-tron/protocols' \
  --network tron:728126428 \
  --token USDT \
  --scheme exact \
  --max-amount 0.000001
```

Equivalent route form:

```text
GET https://x402-gateway.bankofai.io/providers/defillama-tvl-tron/protocols
```

### Base Mainnet

Base Mainnet payments use official USDC with x402 `exact` and EIP-3009:

```bash
curl -sS 'https://x402-gateway.bankofai.io/providers/defillama-tvl-base/protocols'
```

Pay on Base Mainnet with the x402 CLI (amount in USD):

```bash
x402-cli pay 'https://x402-gateway.bankofai.io/providers/defillama-tvl-base/protocols' \
  --method GET \
  --network eip155:8453 \
  --token USDC \
  --scheme exact \
  --max-amount 0.000001
```

## Spend-Aware Usage

- Prefer per-protocol endpoints (/protocol/{slug}, /tvl/{protocol}) over the full /protocols dump to keep payloads small.
- Cache TVL results; these update on the order of minutes, not seconds.

## When Not To Use

- Do not use for real-time token spot prices (DefiLlama price is on a separate host: coins.llama.fi).

## Integration Notes

- Cache responses according to the upstream data freshness needs.
- Prefer specific token, pair, protocol, pool, or address routes over broad dump/search routes when possible.
- Treat market, yield, and security data as decision support, not as the only execution signal.
- The public catalog entry only documents public routes and does not include runtime configuration or wallet material.
