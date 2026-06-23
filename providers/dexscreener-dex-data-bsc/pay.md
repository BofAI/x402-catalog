# DexScreener DEX Pairs & New-Listing API (BSC x402, Free)

Free x402 passthrough for DexScreener token/pair data, search and latest token profiles. New-launch / meme radar data for trading agents. Data by DexScreener.

## Service

- FQN: `dexscreener-dex-data-bsc`
- Gateway base: `https://tm-x402-gateway.bankofai.io/providers/dexscreener-dex-data-bsc`
- Category: `finance`
- Chain: `eip155:56` (BNB Chain)
- Scheme: `exact_permit`
- Tags: dexscreener, dex, new-pairs, meme, liquidity, price, free
- Listed price: free (`0 USD` min and max price)

## When To Use

Use to look up a token's DEX pairs/price/liquidity, search tokens, or pull the latest token profiles for new-launch / meme screening.

## Endpoint Summary

### GET /latest/dex/tokens/{tokenAddresses}

All DEX pairs (price/liquidity/volume/fdv) for one or more token addresses
### GET /latest/dex/search

Search pairs by token name/symbol/address
### GET /token-profiles/latest/v1

Latest token profiles (new-launch / discovery radar)

## Request Examples

- `GET /providers/dexscreener-dex-data-bsc/latest/dex/tokens/{tokenAddresses}`
- `GET /providers/dexscreener-dex-data-bsc/latest/dex/search?q=BNB`
- `GET /providers/dexscreener-dex-data-bsc/token-profiles/latest/v1`

## Response Shape

- Returns DexScreener JSON: pairs with priceUsd, liquidity.usd, volume, fdv, pairCreatedAt, and chain/dex identifiers.

## Code Usage

Call the catalog route with any HTTP client. Example:

```bash
curl -sS 'https://tm-x402-gateway.bankofai.io/providers/dexscreener-dex-data-bsc/latest/dex/search?q=BNB'
```

Equivalent route form:

```text
GET https://tm-x402-gateway.bankofai.io/providers/dexscreener-dex-data-bsc/latest/dex/search?q=BNB
```

## Spend-Aware Usage

- Query by specific token/pair address instead of broad search where possible to reduce payload and noise.
- For new-launch monitoring, poll token-profiles on a sensible interval (not every second); each poll is a paid call.

## When Not To Use

- Do not use as a security check (pair listing != safe); pair with a security provider before trading.

## Integration Notes

- Cache responses according to the upstream data freshness needs.
- Prefer specific token, pair, protocol, pool, or address routes over broad dump/search routes when possible.
- Treat market, yield, and security data as decision support, not as the only execution signal.
- The public catalog entry only documents public routes and does not include runtime configuration or wallet material.
