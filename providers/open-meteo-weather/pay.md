# Open-Meteo Weather API

## Service

- FQN: `open-meteo-weather`
- Service URL: `https://gateway.bankofai.io/providers/open-meteo-weather`
- Category: `data`
- Chains: `eip155:97`

## Endpoints

### GET /v1/forecast

Current weather for latitude and longitude coordinates.

- URL: `https://gateway.bankofai.io/providers/open-meteo-weather/v1/forecast`
- Price: `$0.001`

```bash
x402-cli pay 'https://gateway.bankofai.io/providers/open-meteo-weather/v1/forecast?latitude=31.2304&longitude=121.4737&current=temperature_2m,wind_speed_10m&timezone=auto'
```

## Example Response

```json
{
  "current": {
    "temperature_2m": 25.4,
    "wind_speed_10m": 5.8
  }
}
```

## Notes

This file is public. Do not include upstream API keys, bearer tokens, provider.yml, `.env`, passwords, private keys, or private infrastructure URLs.
