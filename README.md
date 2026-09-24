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

Payment routes support `scheme: exact` with `assetTransferMethod: eip3009` or
`permit2`, and TRON `scheme: exact_gasfree` without an asset transfer method. New TRON routes
must use the decimal CAIP-2 IDs from `@bankofai/x402-tron@2.0.0`:
`tron:728126428` (mainnet), `tron:3448148188` (Nile), and
`tron:2494104990` (Shasta). This applies to both `chains` and route `network`
fields. Legacy hexadecimal IDs such as `tron:0x2b6653dc` and human-readable
aliases such as `tron:nile` are rejected.
With the current x402 SDK, GasFree relayer costs are estimated by the client;
catalog routes must not publish the legacy `fee` or `feeConfig` fields.

Do not submit private configuration or secrets.

## Development and Release Flow

1. Create each feature or fix branch from the latest `develop`.
2. Complete development, validate provider data, rebuild `dist/`, pass the tests,
   and merge the reviewed PR into `develop`.
3. After CI passes on `develop`, tag that commit with `test-v*` to publish the
   Docker `test` image, then deploy it to TN. TN releases must come from
   `develop`, not an unmerged feature branch.
4. Complete TN acceptance before preparing the production release. Commit the
   final generated snapshot and release version references, validate the release
   candidate, then tag and publish it with `v*`. This repository has no npm
   package version.
5. After the production release succeeds, merge the released commit into `main`.
6. Merge `main` back into `develop`, including the released snapshot, version
   references, and fixes, before starting the next development branch.

When introducing this workflow to a repository without `develop`, initialize
`develop` from the current `main` once.

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

`status.json` reports whether the static catalog build completed and how many
providers it contains. A provider detail's `status` object is declared
metadata, not a live health check:

- `catalog`: whether the public entry is listed.
- `gateway`: whether a gateway route is configured.
- `payment`: the declared payment availability (`paid-route`, `mainnet`,
  `testnet`, or `unknown`).
- `upstream`: the declared upstream access mode.

Runtime availability must be checked against the gateway and upstream service.

## Submitting a Provider

1. Run your own x402 gateway and keep all private configuration outside this repository.
2. Add a new directory under `providers/<provider-fqn>/`.
3. Include only `catalog.json` and `pay.md`.
4. Run the build commands above.
5. Open a pull request with the provider metadata and regenerated `dist/` files.

Provider FQNs should be stable, lowercase, and URL-safe.

## Repository Name

The repository name intentionally remains `x402-catelog` for compatibility with the existing project and deployment references.
