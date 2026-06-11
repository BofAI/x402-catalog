# BANK OF AI LLM API

BANK OF AI LLM API is a first-party x402 provider for paid large-language-model inference. It exposes familiar API shapes for model listing, OpenAI-compatible chat completions, and Claude-compatible messages while the gateway handles x402 payment and upstream authentication.

Use it when you want an agent, CLI script, backend service, or test workflow to pay per request and call LLM endpoints without shipping a BANK OF AI upstream API key in the client.

## Service

- FQN: `bankofai-llm`
- Service URL: `https://chat-stg.bankofai.io/chat`
- Category: `ai_ml`
- Chains: `eip155:97`, `tron:nile`
- BSC gateway base: `https://gateway.bankofai.io/providers/bankofai-llm-bsc`
- TRON Nile gateway base: `https://gateway.bankofai.io/providers/bankofai-llm-tron-nile`

## CLI quick start

Install or update the x402 CLI, then use `x402-cli pay` against the gateway endpoint URL. The CLI first receives a `402 Payment Required` challenge, signs the payment with your configured wallet, retries the request with the payment header, and prints the upstream response.

```bash
x402-cli pay 'https://gateway.bankofai.io/providers/bankofai-llm-bsc/v1/models' \
  --network eip155:97 \
  --token USDT \
  --scheme exact_permit
```

TRON Nile is exposed through a separate gateway provider route because the gateway binds one payment network per provider:

```bash
x402-cli pay 'https://gateway.bankofai.io/providers/bankofai-llm-tron-nile/v1/models' \
  --network tron:nile \
  --token USDT \
  --scheme exact_gasfree
```

For JSON APIs, pass the HTTP method and request body:

```bash
x402-cli pay 'https://gateway.bankofai.io/providers/bankofai-llm-bsc/v1/chat/completions' \
  --method POST \
  --network eip155:97 \
  --token USDT \
  --scheme exact_permit \
  --json '{
    "model": "MODEL_ID",
    "messages": [
      {
        "role": "user",
        "content": "Explain x402 payments in one paragraph."
      }
    ]
  }'
```

If your CLI environment supports explicit payment limits, set the maximum amount to the endpoint price or slightly above it. For example:

```bash
x402-cli pay 'https://gateway.bankofai.io/providers/bankofai-llm-bsc/v1/models' \
  --network eip155:97 \
  --token USDT \
  --scheme exact_permit \
  --max-amount 0.001
```

Use the model list response to replace `MODEL_ID` in generation examples.

## Endpoints

### GET /v1/models

List available BANK OF AI LLM models. Use this before generation calls to confirm the model IDs currently exposed by the gateway.

- BSC Testnet URL: `https://gateway.bankofai.io/providers/bankofai-llm-bsc/v1/models`
- TRON Nile URL: `https://gateway.bankofai.io/providers/bankofai-llm-tron-nile/v1/models`
- Price: `$0.001`

```bash
x402-cli pay 'https://gateway.bankofai.io/providers/bankofai-llm-bsc/v1/models' \
  --network eip155:97 \
  --token USDT \
  --scheme exact_permit
```

### POST /v1/chat/completions

Create an OpenAI-compatible chat completion from a `model` and `messages` array. This is the recommended endpoint for OpenAI-style clients, agent loops, and general assistant responses.

- BSC Testnet URL: `https://gateway.bankofai.io/providers/bankofai-llm-bsc/v1/chat/completions`
- TRON Nile URL: `https://gateway.bankofai.io/providers/bankofai-llm-tron-nile/v1/chat/completions`
- Price: `$0.01`

```bash
x402-cli pay 'https://gateway.bankofai.io/providers/bankofai-llm-bsc/v1/chat/completions' \
  --method POST \
  --network eip155:97 \
  --token USDT \
  --scheme exact_permit \
  --json '{"model":"MODEL_ID","messages":[{"role":"user","content":"hello"}]}'
```

### POST /v1/messages

Create a Claude-compatible response with an Anthropic-style request body. Use this when your application already formats prompts as `messages` plus `max_tokens`.

- BSC Testnet URL: `https://gateway.bankofai.io/providers/bankofai-llm-bsc/v1/messages`
- TRON Nile URL: `https://gateway.bankofai.io/providers/bankofai-llm-tron-nile/v1/messages`
- Price: `$0.01`

```bash
x402-cli pay 'https://gateway.bankofai.io/providers/bankofai-llm-tron-nile/v1/messages' \
  --method POST \
  --network tron:nile \
  --token USDT \
  --scheme exact_gasfree \
  --json '{"model":"claude-sonnet-4-6","max_tokens":1024,"messages":[{"role":"user","content":"hello"}]}'
```

## Integration notes

- The catalog `service_url` points to the staging chat entry page: `https://chat-stg.bankofai.io/chat`.
- The endpoint URLs above are the x402 gateway URLs that the CLI should call.
- Gateway currently exposes one payment network per provider route: `bankofai-llm-bsc` for BSC Testnet and `bankofai-llm-tron-nile` for TRON Nile.
- The public catalog does not contain upstream credentials. The gateway operator keeps the BANK OF AI upstream key in the gateway runtime.
- Current listed prices are fixed per request for the test catalog. Usage-based settlement can be added later without changing the public discovery shape.

## Notes

This file is public and must not include API keys, bearer tokens, provider.yml, `.env`, passwords, private keys, or private infrastructure URLs.
