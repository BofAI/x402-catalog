# DIA Multi-Source Token Price API (TRON x402, Free)

Free x402 passthrough for DIA real-time token quotations (3000+ assets, 80+ markets, key-free). Manipulation-resistant price source for agents. Data by DIA.

## Service

- FQN: `dia-price-tron`
- Gateway base: `https://tm-x402-gateway.bankofai.io/providers/dia-price-tron`
- Category: `finance`
- Chain: `tron:mainnet` (TRON)
- Scheme: `exact_gasfree`
- Tags: dia, price, oracle, quotation, multi-source, free
- Listed price: free (`0 USD` min and max price)

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
curl -sS 'https://tm-x402-gateway.bankofai.io/providers/dia-price-tron/v1/quotation/BTC'
```

Equivalent route form:

```text
GET https://tm-x402-gateway.bankofai.io/providers/dia-price-tron/v1/quotation/BTC
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
