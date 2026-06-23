# GoPlus Token & Address Security API (TRON x402, Free)

Free x402 passthrough for GoPlus Security checks (token security / honeypot, malicious address, approval risk). Powered by GoPlus. Agent-native pre-trade risk control.

## Service

- FQN: `goplus-token-security-tron`
- Gateway base: `https://tm-x402-gateway.bankofai.io/providers/goplus-token-security-tron`
- Category: `finance`
- Chain: `tron:mainnet` (TRON)
- Scheme: `exact_gasfree`
- Tags: goplus, security, honeypot, risk, token-security, free
- Listed price: free (`0 USD` min and max price)

## When To Use

Use before buying a token, approving an allowance, or sending to an address: check if a token is a honeypot/scam, whether an address is malicious, and whether an approval is risky.

## Endpoint Summary

### GET /api/v1/token_security/{chain_id}

Token security report (honeypot, taxes, owner privileges, holders) for one or more contracts
### GET /api/v1/address_security/{address}

Malicious-address check (sanctions, phishing, known scam)
### GET /api/v1/approval_security/{chain_id}

Approval / allowance risk check for a spender contract

## Request Examples

- `GET /providers/goplus-token-security-tron/api/v1/token_security/728126428?contract_addresses=T....`
- `GET /providers/goplus-token-security-tron/api/v1/address_security/T....`

## Response Shape

- Returns GoPlus code/message/result with fields like is_honeypot, buy_tax, sell_tax, is_open_source, owner_address, holder_count, is_blacklisted.

## Code Usage

Call the catalog route with any HTTP client. Example:

```bash
curl -sS 'https://tm-x402-gateway.bankofai.io/providers/goplus-token-security-tron/api/v1/token_security/728126428?contract_addresses=T....'
```

Equivalent route form:

```text
GET https://tm-x402-gateway.bankofai.io/providers/goplus-token-security-tron/api/v1/token_security/728126428?contract_addresses=T....
```

## Spend-Aware Usage

- Free endpoint, but still batch multiple contract addresses in one call where the upstream allows it.
- Cache results per (chain_id, contract) for a few minutes; token security rarely changes intra-session.

## When Not To Use

- Do not use as a price source (use a price provider).

## Integration Notes

- Cache responses according to the upstream data freshness needs.
- Prefer specific token, pair, protocol, pool, or address routes over broad dump/search routes when possible.
- Treat market, yield, and security data as decision support, not as the only execution signal.
- The public catalog entry only documents public routes and does not include runtime configuration or wallet material.
