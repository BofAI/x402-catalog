# x402 Catalog Submission Examples

## 中文说明

这里说明服务方如何向公开 Catalog 仓库提交资料。Catalog 仓库只保存公开发现数据，不保存任何私有运行时配置。

服务方流程：

1. 自己启动 Gateway，并把 `provider.yml`、API key、钱包私钥留在自己的运行环境。
2. 使用 `x402-cli catalog export-gateway` 导出公开文件。
3. 只提交 `providers/<fqn>/catalog.json` 和 `providers/<fqn>/pay.md`。
4. 提 PR，CI 会校验字段和敏感信息。

不要提交：

- `provider.yml`
- `.env`
- 上游 API key
- bearer token
- 钱包私钥
- 内网地址

## English

This repository stores public discovery data for x402 providers. It does not
store provider secrets, upstream API keys, private gateway configuration, or
`provider.yml` files.

## Provider Layout

Each submitted provider uses this layout:

```text
providers/<fqn>/catalog.json
providers/<fqn>/pay.md
```

Generated static output:

```text
dist/catalog.json
dist/providers/<fqn>.json
dist/pay/<fqn>.json
dist/pay/<fqn>.md
dist/search-index.json
dist/status.json
```

## 1. Provider Generates Public Files

The provider runs their own gateway first, then exports public files:

```bash
x402-cli catalog export-gateway https://gateway.example.com \
  --provider <fqn> \
  --output-dir providers/<fqn>
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
validated 5 provider(s)
built 5 provider(s) into dist
```

## 4. Consumer Search

After build, consumers and agents can search:

```bash
x402-cli catalog search defi --catalog dist/catalog.json --json
x402-cli catalog show defillama --catalog dist/catalog.json --json
x402-cli catalog endpoints defillama --catalog dist/catalog.json --json
x402-cli catalog pay-json defillama --catalog dist/catalog.json
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

## 6. Run the Catalog Container

```bash
docker compose build catalog
docker compose up -d catalog
curl http://127.0.0.1:8088/api/status.json
curl http://127.0.0.1:8088/api/catalog.json
```
