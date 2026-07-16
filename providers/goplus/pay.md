# GoPlus Token & Address Security API (TRON x402, Paid)

x402-paid passthrough for GoPlus Security checks (token security / honeypot, malicious address, approval risk). Powered by GoPlus. Agent-native pre-trade risk control.

## Service

- FQN: `goplus-token-security-tron`
- Gateway base: `https://x402-gateway.bankofai.io/providers/goplus-token-security-tron`
- Category: `finance`
- Chain: `tron:0x2b6653dc` (TRON)
- Scheme: `exact` + `permit2`
- Tags: goplus, security, honeypot, risk, token-security
- Listed price: `0.000001 USD` per request

## When To Use

Use before buying a token, approving an allowance, or sending to an address: check if a token is a honeypot/scam, whether an address is malicious, and whether an approval is risky.

## Endpoint Summary

### GET /api/v1/token_security/{chain_id}

Token security report (honeypot, taxes, owner privileges, holders) for one or more contracts
### GET /api/v1/address_security/{address}

Malicious-address check (sanctions, phishing, known scam)
### GET /api/v2/token_approval_security/{chain_id}

Token approval / allowance risk check for one or more wallet addresses. Pass `addresses` as a query parameter.

## Request Examples

- `GET /providers/goplus-token-security-tron/api/v1/token_security/728126428?contract_addresses=T....`
- `GET /providers/goplus-token-security-tron/api/v1/address_security/T....`
- `GET /providers/goplus-token-security-tron/api/v2/token_approval_security/728126428?addresses=T....`

## Response Shape

- Returns GoPlus code/message/result with fields like is_honeypot, buy_tax, sell_tax, is_open_source, owner_address, holder_count, is_blacklisted.

## Code Usage

Call the catalog route with any HTTP client. Example:

```bash
curl -sS 'https://x402-gateway.bankofai.io/providers/goplus-token-security-tron/api/v1/token_security/728126428?contract_addresses=T....'
```

Equivalent route form:

```text
GET https://x402-gateway.bankofai.io/providers/goplus-token-security-tron/api/v1/token_security/728126428?contract_addresses=T....
```

## Spend-Aware Usage

- Batch multiple contract addresses in one paid call where the upstream allows it.
- Cache results per (chain_id, contract) for a few minutes; token security rarely changes intra-session.

## When Not To Use

- Do not use as a price source (use a price provider).

## Integration Notes

- Cache responses according to the upstream data freshness needs.
- Prefer specific token, pair, protocol, pool, or address routes over broad dump/search routes when possible.
- Treat market, yield, and security data as decision support, not as the only execution signal.
- The public catalog entry only documents public routes and does not include runtime configuration or wallet material.
