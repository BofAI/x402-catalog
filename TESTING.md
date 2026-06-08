# x402 Catalog 测试说明

本文档给前端、测试和联调人员使用。只需要这个仓库就可以验证 Catalog Server 的列表、详情、搜索索引和 pay-json 输出。

## 1. 测试目标

验证以下闭环：

1. 仓库里的 `providers/<fqn>/catalog.json` 和 `providers/<fqn>/pay.md` 可以通过校验。
2. 构建脚本可以生成 `dist/` 静态快照。
3. Catalog Server 可以通过 `/api/*` 提供给前端。
4. 前端可以读取服务列表、服务详情、分类、搜索索引和 pay-json。
5. `x402-cli catalog` 可以使用同一份 `dist/catalog.json` 搜索和展示服务。

Catalog 一期不使用数据库，不保存用户 API key、钱包私钥、`provider.yml`、`.env` 或任何上游服务密钥。

## 2. 准备环境

需要：

```text
Python 3.12+
Docker
Docker Compose
x402-cli
```

切到测试分支：

```bash
git checkout test/open-meteo-catalog-flow
```

如果本地没有这个分支：

```bash
git fetch origin
git checkout test/open-meteo-catalog-flow
```

## 3. 本地校验

运行：

```bash
python3 scripts/validate.py
python3 scripts/build.py
```

期望看到类似输出：

```text
validated 2 provider(s)
built 2 provider(s) into dist
```

生成物包括：

```text
dist/catalog.json
dist/categories.json
dist/search-index.json
dist/status.json
dist/providers/open-meteo-weather.json
dist/pay/open-meteo-weather.json
dist/pay/open-meteo-weather.md
```

## 4. 启动 Catalog Server

默认端口是 `8088`：

```bash
docker compose build catalog
docker compose up -d catalog
```

检查容器：

```bash
docker compose ps catalog
```

期望状态包含：

```text
healthy
```

检查接口：

```bash
curl http://127.0.0.1:8088/api/status.json
curl http://127.0.0.1:8088/api/catalog.json
curl http://127.0.0.1:8088/api/providers/open-meteo-weather.json
curl http://127.0.0.1:8088/api/pay/open-meteo-weather.json
```

`status.json` 期望包含：

```json
{
  "status": "ok",
  "provider_count": 2,
  "version": 1
}
```

如果需要换端口：

```bash
X402_CATALOG_PORT=8090 docker compose up -d catalog
```

对应访问地址：

```text
http://127.0.0.1:8090/api
```

## 5. 前端调试

前端本地开发使用：

```text
http://127.0.0.1:8088/api
```

Vite 示例：

```bash
VITE_X402_CATALOG_API=http://127.0.0.1:8088/api
```

Next.js 示例：

```bash
NEXT_PUBLIC_X402_CATALOG_API=http://127.0.0.1:8088/api
```

前端列表页读取：

```text
GET /api/catalog.json
GET /api/categories.json
GET /api/search-index.json
```

服务详情页读取：

```text
GET /api/providers/<fqn>.json
GET /api/pay/<fqn>.json
GET /api/pay/<fqn>.md
```

测试 provider：

```text
open-meteo-weather
```

详情接口：

```text
GET /api/providers/open-meteo-weather.json
```

pay-json 接口：

```text
GET /api/pay/open-meteo-weather.json
```

前端渲染建议：

```text
title / subtitle / description / use_case 使用英文默认字段
i18n.zh-CN.title / subtitle / description / useCase 用于中文展示
chains 用于展示支持链
featured_tags 用于标签
endpoints 用于详情页接口列表
status 用于展示 catalog、gateway、payment、upstream 状态
```

## 6. CLI 验证

使用本地构建出的 catalog：

```bash
x402-cli catalog search meteo --catalog dist/catalog.json --json
x402-cli catalog show open-meteo-weather --catalog dist/catalog.json --json
x402-cli catalog endpoints open-meteo-weather --catalog dist/catalog.json --json
x402-cli catalog pay-json open-meteo-weather --catalog dist/catalog.json
```

期望：

```text
search 能返回 open-meteo-weather
show 能返回完整服务详情
endpoints 能返回 GET /v1/forecast
pay-json 能返回 agent/CLI 可读的支付调用摘要
```

## 7. 验收标准

测试通过需要满足：

1. `python3 scripts/validate.py` 成功。
2. `python3 scripts/build.py` 成功。
3. `docker compose ps catalog` 显示服务 healthy。
4. `/api/status.json` 返回 `status: ok`。
5. `/api/catalog.json` 里包含 `open-meteo-weather`。
6. `/api/providers/open-meteo-weather.json` 包含双语标题、副标题、描述、endpoint、chains 和 status。
7. `/api/pay/open-meteo-weather.json` 能被前端、Agent 或 CLI 读取。
8. `x402-cli catalog search meteo --catalog dist/catalog.json --json` 能搜到 `open-meteo-weather`。

## 8. 安全检查

提交 PR 前确认没有以下内容：

```text
provider.yml
.env
API key
bearer token
wallet private key
mnemonic
password
private internal URL
```

仓库只保存公开展示和公开调用所需的信息。上游鉴权、支付收款地址、私钥、环境变量都应该留在 provider 自己运行的 gateway 环境里。

## 9. 停止服务

```bash
docker compose down
```
