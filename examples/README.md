# x402 Catalog Submission Examples

This repository stores public discovery data for x402 providers. It does not
store provider secrets, upstream API keys, private gateway configuration, or
`provider.yml` files.

## Demo Provider

The included demo provider is:

```text
providers/acme-weather/catalog.json
providers/acme-weather/pay.md
```

Generated static output:

```text
dist/catalog.json
dist/providers/acme-weather.json
dist/pay/acme-weather.json
dist/pay/acme-weather.md
dist/search-index.json
dist/status.json
```

## 1. Provider Generates Public Files

The provider runs their own gateway first, then exports public files:

```bash
x402-cli catalog export-gateway https://gateway.example.com \
  --provider acme-weather \
  --output-dir providers/acme-weather
```

The output must contain only:

```text
providers/<fqn>/catalog.json
providers/<fqn>/pay.md
```

## 2. Submit a Pull Request

Copy those files into this repository:

```text
providers/<fqn>/catalog.json
providers/<fqn>/pay.md
```

Do not submit:

```text
provider.yml
.env
upstream API keys
bearer tokens
wallet private keys
passwords
private internal URLs
```

## 3. Validate Locally

```bash
python3 scripts/validate.py
python3 scripts/build.py
```

Expected output:

```text
validated 1 provider(s)
built 1 provider(s) into dist
```

## 4. Consumer Search

After build, consumers and agents can search:

```bash
x402-cli catalog search weather --catalog dist/catalog.json --json
x402-cli catalog show acme-weather --catalog dist/catalog.json --json
x402-cli catalog endpoints acme-weather --catalog dist/catalog.json --json
x402-cli catalog pay-json acme-weather --catalog dist/catalog.json
```

## 5. Frontend Usage

Frontend list page reads:

```text
GET /api/catalog.json
GET /api/categories.json
GET /api/search-index.json
```

Provider detail page reads:

```text
GET /api/providers/<fqn>.json
GET /api/pay/<fqn>.json
```

The current static server shape maps those files from `dist/`.
