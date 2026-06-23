# DefiLlama DeFi Data API (TVL / Fees / Stablecoins) (BSC x402, Free)

Free x402 passthrough for DefiLlama protocol TVL, fees/revenue and stablecoin data. Key-free DeFi decision data layer for agents. Data by DefiLlama.

## Service

- FQN: `defillama-tvl-bsc`
- Gateway base: `https://tm-x402-gateway.bankofai.io/providers/defillama-tvl-bsc`
- Category: `finance`
- Chain: `eip155:56` (BNB Chain)
- Scheme: `exact_permit`
- Tags: defillama, defi, tvl, fees, stablecoins, free
- Listed price: free (`0 USD` min and max price)

## When To Use

Use to read protocol TVL, fees/revenue and stablecoin metrics for DeFi research, allocation or risk screening.

## Endpoint Summary

### GET /protocols

All protocols with current TVL, category and chain breakdown
### GET /protocol/{slug}

Single protocol: historical TVL, fees, tokens, metadata
### GET /tvl/{protocol}

Current total TVL of a protocol (lightweight)

## Request Examples

- `GET /providers/defillama-tvl-bsc/protocols`
- `GET /providers/defillama-tvl-bsc/protocol/pancakeswap-amm`
- `GET /providers/defillama-tvl-bsc/tvl/pancakeswap-amm`

## Response Shape

- Returns DefiLlama JSON: protocol list with tvl/chainTvls/category, or a single protocol's historical TVL, fees and metadata.

## Code Usage

Call the catalog route with any HTTP client. Example:

```bash
curl -sS 'https://tm-x402-gateway.bankofai.io/providers/defillama-tvl-bsc/protocols'
```

Equivalent route form:

```text
GET https://tm-x402-gateway.bankofai.io/providers/defillama-tvl-bsc/protocols
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
