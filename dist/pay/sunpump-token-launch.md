# SunPump Agent Token Launch API

SunPump Agent Token Launch API is an x402-paid gateway provider for launching a SunPump token from structured metadata. It exposes the same launch request shape across TRON Mainnet and BNB Smart Chain payment routes.

Use it when an agent, backend workflow, or CLI script has validated launch metadata and is ready to create a token through a paid API call.

## Service

- FQN: `sunpump-token-launch`
- Service URL: `https://sunpump.meme`
- Category: `finance`
- Chains: `tron:mainnet`, `eip155:56`
- TRON Mainnet gateway base: `https://x402-gateway.bankofai.io/providers/sunpump-token-launch-tron`
- BNB Smart Chain gateway base: `https://x402-gateway.bankofai.io/providers/sunpump-token-launch-bsc`

## CLI Quick Start

Install or update the x402 CLI, then call the route matching the payment chain you want to use.

TRON Mainnet:

```bash
x402-cli pay 'https://x402-gateway.bankofai.io/providers/sunpump-token-launch-tron/pump-api/ai/agentTokenLaunch' \
  --method POST \
  --network tron:mainnet \
  --token USDT \
  --scheme exact \
  --max-amount 0.000001 \
  --header 'Content-Type: application/json' \
  --body '{"name":"X402MainA","symbol":"X4M17","description":"x402 launch","imageBase64":"","twitterUrl":"","telegramUrl":"","websiteUrl":"","tweetUsername":""}'
```

BNB Smart Chain:

```bash
x402-cli pay 'https://x402-gateway.bankofai.io/providers/sunpump-token-launch-bsc/pump-api/ai/agentTokenLaunch' \
  --method POST \
  --network eip155:56 \
  --token USDT \
  --scheme exact \
  --max-amount 0.000001 \
  --header 'Content-Type: application/json' \
  --body '{"name":"X402BscA","symbol":"X4B17","description":"x402 launch","imageBase64":"","twitterUrl":"","telegramUrl":"","websiteUrl":"","tweetUsername":""}'
```

## Endpoint

### POST /pump-api/ai/agentTokenLaunch

Create a SunPump token from JSON metadata after x402 payment settlement.

Required request fields:

- `name`: token name, 1-20 characters.
- `symbol`: token symbol. Use a unique value.
- `description`: token description.
- `imageBase64`: optional base64-encoded token image. Leave it empty or omit it to let SunPump generate an image automatically.
- `twitterUrl`, `telegramUrl`, `websiteUrl`: optional social links, or empty strings.
- `tweetUsername`: optional tweet username, or an empty string.

The upstream response returns SunPump status and token launch data such as token id, owner address, contract address, create transaction hash, logo URL, reserves, and market data when available.

## Integration Notes

- The endpoint has side effects: a successful paid call can create a token.
- Validate metadata before paying. In particular, keep `name` within 1-20 characters.
- You can provide your own token image with `imageBase64`; otherwise the launch service generates one.
- Current listed prices are fixed per request across both mainnet payment routes.
- The public catalog does not contain gateway runtime secrets or wallet keys.
