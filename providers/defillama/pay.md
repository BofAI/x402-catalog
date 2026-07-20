# DefiLlama DeFi Data API (TRON and BSC x402, Paid)

x402-paid passthrough for DefiLlama protocol TVL, fees/revenue and stablecoin data. Paid DeFi decision data layer for agents. Data by DefiLlama.

## Service

- Catalog FQN: `defillama`
- Gateway providers: `defillama-tvl-tron`, `defillama-tvl-bsc`
- Category: `finance`
- Chains: `tron:0x2b6653dc` (TRON), `eip155:56` (BNB Smart Chain)
- Schemes: `exact` + `permit2` (default), `exact_gasfree`
- Tags: defillama, defi, tvl, fees, stablecoins
- Listed price: `0.000001 USD` per request

## When To Use

Use to read protocol TVL, fees/revenue and stablecoin metrics for DeFi research, allocation or risk screening.

## Endpoint Summary

### GET /protocols

All protocols with current TVL, category and chain breakdown
### GET /protocol/{slug}

Single protocol: historical TVL, fees, tokens, metadata
### GET /tvl/{protocol}

Current total TVL of a protocol (lightweight)

### Prices and yields

The catalog also publishes current/historical prices, price charts, percentage changes, yield pools, and pool-history endpoints. Use the matching `x402Routes` entry in the machine-readable pay JSON for the selected chain.

## Request Examples

- `GET /providers/defillama-tvl-tron/protocols`
- `GET /providers/defillama-tvl-tron/protocol/sunswap-v3`
- `GET /providers/defillama-tvl-tron/tvl/sunswap-v3`

## Response Shape

- Returns DefiLlama JSON: protocol list with tvl/chainTvls/category, or a single protocol's historical TVL, fees and metadata.

## Code Usage

Call the catalog route with any HTTP client. Example:

```bash
curl -sS 'https://x402-gateway.bankofai.io/providers/defillama-tvl-tron/protocols'
```

Pay with the default TRON Permit2 scheme:

```bash
x402-cli pay 'https://x402-gateway.bankofai.io/providers/defillama-tvl-tron/protocols' \
  --network tron:0x2b6653dc \
  --token USDT \
  --scheme exact \
  --max-amount 0.000001
```

Equivalent route form:

```text
GET https://x402-gateway.bankofai.io/providers/defillama-tvl-tron/protocols
```

## Spend-Aware Usage

- Prefer per-protocol endpoints (/protocol/{slug}, /tvl/{protocol}) over the full /protocols dump to keep payloads small.
- Cache TVL/fees results; these update on the order of minutes, not seconds.

## When Not To Use

- Do not use for real-time token spot prices (DefiLlama price is on a separate host: coins.llama.fi).

## Integration Notes

- Cache responses according to the upstream data freshness needs.
- Prefer specific token, pair, protocol, pool, or address routes over broad dump/search routes when possible.
- Treat market, yield, and security data as decision support, not as the only execution signal.
- The public catalog entry only documents public routes and does not include runtime configuration or wallet material.
