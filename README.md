# x402 Catalog

`x402-catelog` is a public service catalog for x402-enabled APIs.

The repository stores only public discovery metadata. It does not store gateway runtime configuration, upstream API keys, bearer tokens, wallet private keys, `provider.yml`, `.env` files, or other private operator data.

## What This Repository Contains

Provider entries live under `providers/`:

```text
providers/<provider-fqn>/catalog.json
providers/<provider-fqn>/pay.md
```

Generated catalog snapshots live under `dist/`:

```text
dist/catalog.json
dist/providers/<provider-fqn>.json
dist/pay/<provider-fqn>.json
dist/pay/<provider-fqn>.md
dist/categories.json
dist/search-index.json
dist/status.json
```

The generated files are static JSON and Markdown assets that can be served by any static file server or CDN.

## Provider Metadata

Each provider directory contains two public files:

- `catalog.json`: service metadata for catalog UIs, CLI tools, and agents.
- `pay.md`: human-readable usage and payment instructions.

Provider metadata should describe the public service surface only:

- service name, logo, category, and tags
- supported chains and payment routes
- public endpoint paths, methods, and descriptions
- pricing summary
- localized display metadata when available

Payment routes support `scheme: exact` with `assetTransferMethod: permit2`, and
TRON `scheme: exact_gasfree` without an asset transfer method. New TRON routes
should use canonical CAIP-2 IDs such as `tron:0x2b6653dc` (mainnet) and
`tron:0xcd8690dc` (Nile); legacy aliases remain readable during migration.
With x402 SDK 1.0.1-beta.4, GasFree relayer costs are estimated by the client;
catalog routes must not publish the legacy `fee` or `feeConfig` fields.

Do not submit private configuration or secrets.

## Build

Requirements:

- Python 3.11 or newer

Build the static catalog:

```bash
python3 scripts/validate.py
python3 scripts/build.py
```

The build reads `providers/*/catalog.json` and writes the generated snapshot into `dist/`.

## Public API Shape

When `dist/` is served under `/api`, consumers can read:

```text
GET /api/status.json
GET /api/catalog.json
GET /api/categories.json
GET /api/search-index.json
GET /api/providers/<provider-fqn>.json
GET /api/pay/<provider-fqn>.json
GET /api/pay/<provider-fqn>.md
```

`catalog.json` is the primary index for catalog UIs and agent discovery. Provider detail pages can use `providers/<provider-fqn>.json`, while CLI and agent payment flows can use `pay/<provider-fqn>.json` or `pay/<provider-fqn>.md`.

## Submitting a Provider

1. Run your own x402 gateway and keep all private configuration outside this repository.
2. Add a new directory under `providers/<provider-fqn>/`.
3. Include only `catalog.json` and `pay.md`.
4. Run the build commands above.
5. Open a pull request with the provider metadata and regenerated `dist/` files.

Provider FQNs should be stable, lowercase, and URL-safe.

## Repository Name

The repository name intentionally remains `x402-catelog` for compatibility with the existing project and deployment references.
