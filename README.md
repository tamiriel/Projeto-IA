# AI-Assisted Financial Scenarios API

**Python · Flask · Gemini API · JSON**

An **experimental academic prototype** that accepts financial data via a Flask HTTP endpoint and asks a large language model (LLM) to return a structured, exploratory comparison of tax scenarios.

> **Status: prototype.** This repository does **not** implement a validated tax engine, deterministic fiscal calculations or a tested ARIMA forecasting model. Generated numbers may be inaccurate and must not be used for accounting, fiscal decisions or professional advice.

## What this repository demonstrates

- Implementing a JSON HTTP endpoint with Flask
- Calling an external generative AI API
- Parsing model output as JSON and handling invalid responses
- Handling API credentials through environment variables
- Documenting an experimental integration and its limitations

## Architecture

```text
Client (JSON)
    |
    v
POST /chat  --> Flask input validation
    |
    v
Gemini model (external API)
    |
    v
Parse model output as JSON
    |
    v
JSON response or HTTP error
```

The model generates an analysis; the application **does not independently verify** the mathematical or legal correctness of that analysis.

## Requirements

- Python 3.10+
- A Google Gemini API key
- Internet access for calls to the model

## Run locally

```bash
git clone https://github.com/tamiriel/Projeto-IA.git
cd Projeto-IA
python -m venv .venv
```

Activate the environment:

- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

Then:

```bash
pip install -r requirements.txt
```

Set `GOOGLE_API_KEY` in the shell (do not commit the actual value). For example, in PowerShell:

```powershell
$env:GOOGLE_API_KEY="YOUR_API_KEY"
python app.py
```

On macOS/Linux:

```bash
export GOOGLE_API_KEY="YOUR_API_KEY"
python app.py
```

By default, the local API listens at `http://127.0.0.1:5000`. The `.env.example` file documents the expected variable; the application reads it from the process environment and does not automatically load `.env`.

## Example request

```bash
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"companyId":123,"year":2026,"historicalMonthly":[{"ano":2025,"mes":12,"receitaBruta":"48000.00"}]}'
```

**Response:** a JSON object produced by the model, potentially containing `companyId`, `year`, `metodo`, `observacoes`, `regimes` and `recomendado`. Exact contents vary between calls; no fixed output or fiscal accuracy is guaranteed.

### HTTP errors

| Status | Meaning |
| --- | --- |
| 400 | Missing, malformed or non-object JSON input |
| 503 | No API key configured on the server |
| 502 | Invalid model response or external model request failure |

## Known limitations

- The integration uses a prompt rather than a verified, versioned calculation engine.
- LLM outputs can be inconsistent, hallucinated or legally out of date.
- There is currently no formal input schema or automated integration-test suite.
- There is no rate limiting, authentication, audit trail or production deployment setup.
- The included CI workflow checks Python syntax only; it is **not** a test suite.
- Sending company data to an external model requires data-governance and privacy review.

## Next engineering steps

- [ ] Add a request schema with field-level validation
- [ ] Add unit tests with the Gemini client mocked
- [ ] Separate Flask routing from model integration
- [ ] Validate model output against a defined response schema
- [ ] Establish deterministic, independently tested fiscal rules before presenting comparisons as reliable
- [ ] Add request limits and production-ready error handling
- [ ] Document data handling and privacy risks

## Author

**Tainara da Rosa** · Computer Engineering · [GitHub](https://github.com/tamiriel)
