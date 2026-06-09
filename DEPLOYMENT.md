# x402 Catalog 测试环境部署

本文档用于部署 Catalog 测试环境，并说明它如何和 Gateway、前端联调。Catalog 一期是静态 JSON 服务，不需要数据库，不保存用户 API key、钱包私钥、`provider.yml` 或 `.env`。

## 1. 部署目标

测试环境建议拆成两个服务：

```text
Catalog TN: https://catalog-tn.example.com/api
Gateway TN: https://gateway-tn.example.com
```

前端只配置 Catalog API：

```text
VITE_X402_CATALOG_API=https://catalog-tn.example.com/api
```

Catalog 返回 provider 列表和 endpoint URL；真正调用 API 时，前端或 CLI 使用 catalog 返回的 `endpoint.url`，也就是 Gateway 地址。

## 2. 部署 Catalog

拉取代码：

```bash
git clone git@github.com:BofAI/x402-catelog.git
cd x402-catelog
git checkout test/open-meteo-catalog-flow
```

本地校验：

```bash
python3 scripts/validate.py
python3 scripts/build.py
```

构建并启动容器：

```bash
docker compose build catalog
docker compose up -d catalog
```

也可以直接使用 CI 推送的 Catalog 镜像：

```bash
export X402_CATALOG_IMAGE=ghcr.io/bofai/x402-catelog:tn-test-20260609-bankofai-llm-api-images
docker compose pull catalog
docker compose up -d --no-build catalog
```

日志路径：

```text
容器内：/app/log/catalog.log
宿主机：./log/catalog.log
```

查看日志：

```bash
docker compose logs -f catalog
tail -f ./log/catalog.log
```

默认监听：

```text
0.0.0.0:8088 -> container 8080
```

如果需要改端口：

```bash
X402_CATALOG_PORT=8088 docker compose up -d catalog
```

健康检查：

```bash
curl -fsS http://127.0.0.1:8088/api/status.json
curl -fsS http://127.0.0.1:8088/api/catalog.json
curl -fsS http://127.0.0.1:8088/api/providers/open-meteo-weather.json
curl -fsS http://127.0.0.1:8088/api/pay/open-meteo-weather.json
```

期望：

```text
/api/status.json 返回 status=ok
/api/catalog.json 返回 providers
/api/providers/open-meteo-weather.json 返回 title_zh、main_title、sub_title、chain_kinds、category_meta
```

## 3. 反向代理

测试环境需要把外部域名转发到本机 `8088`。

Nginx 示例：

```nginx
server {
    listen 443 ssl;
    server_name catalog-tn.example.com;

    location /api/ {
        proxy_pass http://127.0.0.1:8088/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

验证：

```bash
curl -fsS https://catalog-tn.example.com/api/status.json
curl -fsS https://catalog-tn.example.com/api/catalog.json
```

## 4. 前端配置

Vite：

```bash
VITE_X402_CATALOG_API=https://catalog-tn.example.com/api
```

Next.js：

```bash
NEXT_PUBLIC_X402_CATALOG_API=https://catalog-tn.example.com/api
```

前端主要读取：

```text
GET /api/catalog.json
GET /api/providers/<fqn>.json
GET /api/pay/<fqn>.json
GET /api/categories.json
GET /api/search-index.json
GET /api/status.json
```

注意：接口路径都带 `.json` 或 `.md` 后缀。

## 5. 部署 Gateway

Gateway 不在本仓库。测试环境需要同时部署：

```text
git@github.com:BofAI/x402-gateway.git
branch: feature/0.6.1-gateway-init
```

Catalog 里的 provider endpoint 需要指向 Gateway TN，例如：

```text
https://gateway-tn.example.com/providers/open-meteo-weather/v1/forecast
```

如果 Gateway 域名变化，需要重新生成或更新 Catalog 里的公开文件：

```text
providers/<fqn>/catalog.json
providers/<fqn>/pay.md
dist/*
```

## 6. 测试环境两种模式

### Sandbox 模式

用途：

```text
前端联调
Catalog 列表和详情页联调
Gateway 402 返回联调
不做真实链上支付
```

特点：

```text
可以使用 mock facilitator
不需要真实钱包资金
适合快速部署
```

### 真实测试网支付模式

用途：

```text
BSC Testnet / TRON Nile 上链支付验收
CLI/Agent 端到端验收
```

需要准备：

```text
真实测试网 facilitator URL
真实测试网 recipient 收款地址
测试钱包私钥，只放在 Gateway/CLI 运行环境，不进 Git
测试网 gas 和 token 余额
```

Catalog 仓库仍然只保存公开 `catalog.json` 和 `pay.md`，不保存 `provider.yml` 和任何密钥。

## 7. 发布更新流程

当新增或修改 provider：

```bash
python3 scripts/validate.py
python3 scripts/build.py
docker compose build catalog
docker compose up -d catalog
curl -fsS http://127.0.0.1:8088/api/status.json
```

提交：

```bash
git add providers dist
git commit -m "Update catalog providers"
git push
```

GitHub Actions 会自动：

```text
校验 provider 文件
构建 dist
构建 Docker image
启动容器做 HTTP smoke
上传 dist artifact
```

## 8. 回滚

Catalog 是静态快照，回滚方式是切回上一版 Git commit 后重建容器：

```bash
git checkout <previous-good-commit>
docker compose build catalog
docker compose up -d catalog
curl -fsS http://127.0.0.1:8088/api/status.json
```

## 9. 验收清单

测试环境部署完成需要满足：

```text
Catalog 容器 healthy
https://catalog-tn.example.com/api/status.json 返回 ok
https://catalog-tn.example.com/api/catalog.json 返回 provider_count > 0
open-meteo-weather 详情返回 title_zh/main_title/sub_title
open-meteo-weather 详情返回 chain_kinds/category_meta
前端能读取 Catalog API 并渲染列表和详情
Gateway TN endpoint 可以返回 402 Payment Required
CLI 可以用 x402-cli catalog search/search/show/pay-json 读取 catalog
```

## 10. 当前测试 Provider

```text
fqn: open-meteo-weather
category: data
chain_kinds: bnb
endpoint: GET /v1/forecast
```

测试接口：

```text
GET /api/providers/open-meteo-weather.json
GET /api/pay/open-meteo-weather.json
```
