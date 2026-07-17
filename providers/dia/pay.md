# DIA Multi-Source Token Price API (TRON and BSC x402, Paid)

x402-paid passthrough for DIA real-time token quotations (3000+ assets, 80+ markets, keyless). Manipulation-resistant price source for agents. Data by DIA.

## Service

- Catalog FQN: `dia`
- Gateway providers: `dia-price-tron`, `dia-price-bsc`
- Category: `finance`
- Chains: `tron:0x2b6653dc` (TRON), `eip155:56` (BNB Smart Chain)
- Schemes: `exact` + `permit2` (default), `exact_gasfree`
- Tags: dia, price, oracle, quotation, multi-source
- Listed price: `0.000001 USD` per request

## When To Use

Use to get a real-time, multi-market aggregated USD price for a token by symbol or by blockchain+contract address.

## Endpoint Summary

### GET /v1/quotation/{symbol}

Aggregated price quotation by asset symbol
### GET /v1/assetQuotation/{blockchain}/{address}

Aggregated price quotation by blockchain + contract address

## Request Examples

- `GET /providers/dia-price-tron/v1/quotation/BTC`
- `GET /providers/dia-price-tron/v1/assetQuotation/Tron/{address}`

## Response Shape

- Returns DIA JSON: Symbol, Name, Price, PriceYesterday, VolumeYesterdayUSD, Time, Source.

## Code Usage

Call the catalog route with any HTTP client. Example:

```bash
curl -sS 'https://x402-gateway.bankofai.io/providers/dia-price-tron/v1/quotation/BTC'
```

Pay with the default TRON Permit2 scheme:

```bash
x402-cli pay 'https://x402-gateway.bankofai.io/providers/dia-price-tron/v1/quotation/BTC' \
  --network tron:0x2b6653dc \
  --token USDT \
  --scheme exact \
  --max-amount 0.000001
```

Equivalent route form:

```text
GET https://x402-gateway.bankofai.io/providers/dia-price-tron/v1/quotation/BTC
```

## Spend-Aware Usage

- Request one asset per call; cache short-term as prices update on a seconds-to-minutes cadence.
- Use the on-chain address endpoint for long-tail tokens, the symbol endpoint for majors.

## When Not To Use

- Do not use for DEX-pair-level liquidity/new-launch data (use a DEX data provider).

## Integration Notes

- Cache responses according to the upstream data freshness needs.
- Prefer specific token, pair, protocol, pool, or address routes over broad dump/search routes when possible.
- Treat market, yield, and security data as decision support, not as the only execution signal.
- The public catalog entry only documents public routes and does not include runtime configuration or wallet material.
