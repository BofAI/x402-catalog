# SunPump Agent Token Launch API

SunPump Agent Token Launch API is an x402-paid gateway provider entry for a SunPump launch route. The current upstream POST endpoint returns `405 Not Allowed`, so this route is documented as configured but not currently usable for successful token creation.

Do not use this endpoint for production token creation until SunPump provides an active POST API path.

## Service

- FQN: `sunpump-token-launch`
- Service URL: `https://sunpump.meme`
- Category: `finance`
- Chains: `tron:mainnet`, `eip155:56`
- TRON Mainnet/Nile gateway base: `https://tm-x402-gateway.bankofai.io/providers/sunpump-token-launch-tron`
- BNB Smart Chain gateway base: `https://tm-x402-gateway.bankofai.io/providers/sunpump-token-launch-bsc`

## Current Status

The x402 gateway route can issue a payment challenge, but the upstream SunPump endpoint currently rejects POST requests. A paid call may settle and then return an upstream `405 Not Allowed` response.

## CLI Shape

TRON Mainnet/Nile:

```bash
x402-cli pay 'https://tm-x402-gateway.bankofai.io/providers/sunpump-token-launch-tron/pump-api/ai/agentTokenLaunch' \
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
x402-cli pay 'https://tm-x402-gateway.bankofai.io/providers/sunpump-token-launch-bsc/pump-api/ai/agentTokenLaunch' \
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

Configured launch route for JSON metadata after x402 payment settlement. It is currently blocked by the upstream `405 Not Allowed` response.

Required request fields:

- `name`: token name, 1-20 characters.
- `symbol`: token symbol. Use a unique value.
- `description`: token description.
- `imageBase64`: optional base64-encoded token image. Leave it empty or omit it to let SunPump generate an image automatically.
- `twitterUrl`, `telegramUrl`, `websiteUrl`: optional social links, or empty strings.
- `tweetUsername`: optional tweet username, or an empty string.

When SunPump restores or publishes an active launch API, the upstream response is expected to return launch status and token data. Until then, this endpoint should be treated as unavailable.

## Integration Notes

- The endpoint is currently unavailable because the upstream POST route returns `405 Not Allowed`.
- After SunPump restores an active route, the endpoint may have side effects: a successful paid call can create a token.
- Validate metadata before paying. In particular, keep `name` within 1-20 characters.
- You can provide your own token image with `imageBase64`; otherwise the launch service generates one.
- Current listed prices are fixed per request across both testnet payment routes.
- The public catalog does not contain gateway runtime secrets or wallet keys.
