# Machina — Payment & Usage Guide

**Provider:** mach402.dev  
**Base URL:** https://mach402.dev  
**Docs:** https://mach402.dev/docs  
**Contact:** ceo@difftechstore.com  
**Network:** Base mainnet (eip155:8453)  
**Payment token:** USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`)  
**Payout wallet:** `0x14B21d80bf5776437dD4f1043BDAf31e60B366AD`  
**Payment protocol:** x402 (HTTP 402)

---

## How payments work

All paid endpoints follow the standard x402 handshake:

1. Call the endpoint without a payment header → receive `HTTP 402 Payment Required` with an `accepts` array describing the price, asset, network, and `payTo` address.
2. Sign a USDC transfer for the exact amount and attach it in the `X-PAYMENT` header.
3. Retry the request → receive the real response if payment is valid.

Free endpoints (`/pdf/inspect`, `/.well-known/x402`) bypass payment entirely.

---

## Endpoints

### POST /scan/python — $0.020
Scan Python source code for security issues, quality score, complexity, and CVEs in dependencies.

**Request body:**
```json
{
  "code": "<python source code string>",
  "filename": "example.py"
}
```

**Response:**
```json
{
  "security": { "issues": [...], "severity_counts": {...} },
  "quality": { "score": 8.5, "issues": [...] },
  "complexity": { "average_complexity": 3.2, "functions": [...] },
  "dependencies": { "vulnerabilities": [...], "packages_checked": 5 }
}
```

**Limits:** Max 10,000 lines / 500KB per call.

---

### POST /validate/email — $0.007
Validate a single email address.

**Request body:**
```json
{ "email": "user@example.com" }
```

**Response:**
```json
{
  "email": "user@example.com",
  "valid": true,
  "syntax_ok": true,
  "mx_found": true,
  "disposable": false,
  "role_account": false,
  "catch_all": false,
  "verdict": "deliverable"
}
```

---

### POST /validate/email/bulk — $0.500
Validate up to 100 emails in one call.

**Request body:**
```json
{ "emails": ["a@example.com", "b@example.com"] }
```

**Response:** Array of per-email results in the same format as single validation.

---

### POST /domain/intel — $0.050
Full domain intelligence report.

**Request body:**
```json
{ "domain": "example.com" }
```

**Response:**
```json
{
  "whois": { "registrar": "...", "expiry": "...", "created": "..." },
  "dns": { "a": [...], "mx": [...], "ns": [...], "txt": [...] },
  "ssl": { "issuer": "...", "expires": "...", "san": [...] },
  "email_security": { "spf": "...", "dmarc": "...", "dkim_selector": null },
  "tech_stack": ["Cloudflare", "nginx"]
}
```

---

### POST /pdf/extract — $0.050 (up to 50 pages)
Convert a PDF to clean Markdown text.

**Request body:**
```json
{ "url": "https://example.com/document.pdf" }
```

**Response:**
```json
{
  "markdown": "# Document Title\n\n...",
  "pages": 12,
  "chars": 4821
}
```

**Note:** Rule-based extraction (PyMuPDF) — no OCR, no AI. Scanned/image PDFs will produce empty or poor output. Use `/pdf/inspect` first to check.

---

### POST /pdf/extract/large — $0.180 (up to 200 pages)
Same as `/pdf/extract` but accepts PDFs up to 200 pages.

---

### GET /pdf/inspect — **FREE**
Returns PDF metadata without extracting content. No payment required.

**Request body:**
```json
{ "url": "https://example.com/document.pdf" }
```

**Response:**
```json
{
  "pages": 47,
  "title": "Annual Report 2026",
  "has_text": true,
  "file_size_bytes": 1204832,
  "recommended_endpoint": "/pdf/extract"
}
```

---

### POST /url/extract — $0.005
Fetch a URL and return clean Markdown text (strips ads, nav, boilerplate).

**Request body:**
```json
{ "url": "https://example.com/article" }
```

**Response:**
```json
{
  "url": "https://example.com/article",
  "markdown": "# Article Title\n\n...",
  "chars": 3241,
  "truncated": false
}
```

**Limits:** Max 100,000 characters returned.

---

## Error codes

| HTTP | Meaning |
|------|---------|
| 402 | Payment required — see `accepts` array for price |
| 400 | Bad request — check request body |
| 413 | Payload too large (code scanner: > 500KB) |
| 422 | Unprocessable — e.g. PDF is image-only, URL unreachable |
| 429 | Rate limited — back off and retry |
| 500 | Internal error — retry; contact ceo@difftechstore.com if persistent |

---

## x402 wire format

The 402 response body follows x402 v2:

```json
{
  "x402Version": 2,
  "network": "eip155:8453",
  "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  "payTo": "0x14B21d80bf5776437dD4f1043BDAf31e60B366AD",
  "amount": "20000"
}
```

`amount` is in USDC atomic units (6 decimals): `20000` = $0.020.

---

## Discovery

Machine-readable service manifest: `https://mach402.dev/.well-known/x402`  
OpenAPI spec: `https://mach402.dev/openapi.json`  
Swagger UI: `https://mach402.dev/docs`
