# x402-catelog

`x402-catelog` 是 BankofAI 维护的公开 x402 服务目录仓库。一期不保存数据库，也不接收任何上游 API key、token、password、provider.yml 或 `.env`。

社区提交流程和可复制命令见 [`examples/README.md`](examples/README.md)。
前端和测试环境调试流程见 [`TESTING.md`](TESTING.md)。

服务方自己运行 gateway，向本仓库提交公开材料：

- `providers/<fqn>/catalog.json`：前端、CLI、Agent 用的公开服务信息。
- `providers/<fqn>/pay.md`：人和 Agent 可读的调用与支付说明。

CI 会校验字段、扫描敏感信息，然后生成 `dist/` 静态快照：

- `dist/catalog.json`：前端列表页和 `x402-cli catalog search` 使用。
- `dist/providers/<fqn>.json`：服务详情。
- `dist/pay/<fqn>.json`：Agent/CLI 读取的支付与调用摘要。
- `dist/pay/<fqn>.md`：可读版调用说明。
- `dist/search-index.json`：轻量搜索索引。
- `dist/categories.json`：前端分类配置。
- `dist/status.json`：构建状态。

## 本地校验

```bash
python3 scripts/validate.py
python3 scripts/build.py
```

## 容器启动

Catalog 是静态服务，镜像构建时会先校验并生成 `dist/`，然后从 `/api/` 提供 JSON。

```bash
docker compose build catalog
docker compose up -d catalog
curl http://127.0.0.1:8088/api/status.json
curl http://127.0.0.1:8088/api/catalog.json
```

端口可通过环境变量覆盖：

```bash
X402_CATALOG_PORT=8088 docker compose up -d catalog
```

前端本地开发默认使用：

```text
http://127.0.0.1:8088/api
```

主要接口：

```text
GET /api/status.json
GET /api/catalog.json
GET /api/providers/<fqn>.json
GET /api/pay/<fqn>.json
GET /api/pay/<fqn>.md
GET /api/categories.json
GET /api/search-index.json
```

## 本地搜索 Demo

```bash
x402-cli catalog search weather --catalog dist/catalog.json --json
x402-cli catalog show acme-weather --catalog dist/catalog.json --json
x402-cli catalog endpoints acme-weather --catalog dist/catalog.json --json
x402-cli catalog pay-json acme-weather --catalog dist/catalog.json
```

## 服务方提交流程

1. 在自己的机器运行 gateway，密钥只留在本地 `provider.yml` 或环境变量中。
2. 用 `x402-cli catalog export-gateway` 导出公开的 `catalog.json` 和 `pay.md`。
3. 在本仓库新增 `providers/<fqn>/catalog.json` 与 `providers/<fqn>/pay.md`。
4. 提交 PR，CI 通过后由定时任务或发布流程刷新 `dist/` 到 Catalog Server/CDN。

仓库名沿用现有 `x402-catelog`。
