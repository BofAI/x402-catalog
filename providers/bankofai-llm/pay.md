# BANK OF AI LLM API

## Service

- FQN: `bankofai-llm`
- Service URL: `https://gateway.bankofai.io/providers/bankofai-llm`
- Category: `ai_ml`
- Chains: `eip155:97`

## Endpoints

### GET /v1/models

List available BANK OF AI LLM models.

- URL: `https://gateway.bankofai.io/providers/bankofai-llm/v1/models`
- Price: `$0.001`

```bash
x402-cli pay 'https://gateway.bankofai.io/providers/bankofai-llm/v1/models'
```

### POST /v1/chat/completions

Create a chat completion.

- URL: `https://gateway.bankofai.io/providers/bankofai-llm/v1/chat/completions`
- Price: `$0.01`

```bash
x402-cli pay 'https://gateway.bankofai.io/providers/bankofai-llm/v1/chat/completions' \
  --method POST \
  --json '{"model":"MODEL_ID","messages":[{"role":"user","content":"hello"}]}'
```

### POST /v1/completions

Create a text completion.

- URL: `https://gateway.bankofai.io/providers/bankofai-llm/v1/completions`
- Price: `$0.01`

```bash
x402-cli pay 'https://gateway.bankofai.io/providers/bankofai-llm/v1/completions' \
  --method POST \
  --json '{"model":"MODEL_ID","prompt":"hello"}'
```

### POST /v1/embeddings

Create text embeddings.

- URL: `https://gateway.bankofai.io/providers/bankofai-llm/v1/embeddings`
- Price: `$0.005`

```bash
x402-cli pay 'https://gateway.bankofai.io/providers/bankofai-llm/v1/embeddings' \
  --method POST \
  --json '{"model":"MODEL_ID","input":"hello"}'
```

## Notes

Gateway runtime must configure `BANKOFAI_API_KEY`; this file is public and must not include API keys, bearer tokens, provider.yml, `.env`, passwords, private keys, or private infrastructure URLs.
