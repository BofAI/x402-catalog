# DexScreener DEX Pairs & New-Listing API (TRON, BSC and Base Mainnet x402, Paid)

x402-paid passthrough for DexScreener token/pair data, search and latest token profiles. New-launch / meme radar data for trading agents. Data by DexScreener.

## Service

- Catalog FQN: `dexscreener`
- Gateway providers: `dexscreener-dex-data-tron`, `dexscreener-dex-data-bsc`, `dexscreener-dex-data-base`
- Category: `finance`
- Chains: `tron:728126428` (TRON), `eip155:56` (BNB Smart Chain), `eip155:8453` (Base Mainnet)
- Schemes: TRON/BSC `exact` + Permit2; TRON also supports `exact_gasfree`; Base Mainnet uses `exact` + USDC EIP-3009
- Tags: dexscreener, dex, new-pairs, meme, liquidity, price
- Listed price: `0.000001 USD` per request

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

- `GET /providers/dexscreener-dex-data-tron/latest/dex/tokens/{tokenAddresses}`
- `GET /providers/dexscreener-dex-data-tron/latest/dex/search?q=SUN`
- `GET /providers/dexscreener-dex-data-tron/token-profiles/latest/v1`

## Response Shape

- Returns DexScreener JSON: pairs with priceUsd, liquidity.usd, volume, fdv, pairCreatedAt, and chain/dex identifiers.

## Code Usage

Call the catalog route with any HTTP client. Example:

```bash
curl -sS 'https://x402-gateway.bankofai.io/providers/dexscreener-dex-data-tron/latest/dex/search?q=SUN'
```

Pay with the default TRON Permit2 scheme:

```bash
x402-cli pay 'https://x402-gateway.bankofai.io/providers/dexscreener-dex-data-tron/latest/dex/search?q=SUN' \
  --network tron:728126428 \
  --token USDT \
  --scheme exact \
  --max-amount 0.000001
```

Equivalent route form:

```text
GET https://x402-gateway.bankofai.io/providers/dexscreener-dex-data-tron/latest/dex/search?q=SUN
```

### Base Mainnet

```bash
x402-cli pay 'https://x402-gateway.bankofai.io/providers/dexscreener-dex-data-base/latest/dex/search?q=USDC' \
  --network eip155:8453 \
  --token USDC \
  --scheme exact \
  --max-amount 0.000001
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
