# Colombia TRM

Official Colombian USD/COP TRM (Tasa Representativa del Mercado) from Superintendencia Financiera, served as prepaid x402 JSON.

## Pay

- URL: `https://x402.lagaceta.net/trm`
- Method: `GET`
- Network: Base mainnet `eip155:8453`
- Asset: USDC
- Scheme: `exact` + EIP-3009
- Price: `$0.005` per call

Unpaid requests return HTTP 402.

```bash
curl -sS -D- https://x402.lagaceta.net/trm
```

Discovery:

- `https://x402.lagaceta.net/.well-known/x402`
- `https://x402.lagaceta.net/openapi.json`

Source: Superintendencia Financiera dataset `mcec-87by` on datos.gov.co. The endpoint fails closed if the official series is unavailable.
