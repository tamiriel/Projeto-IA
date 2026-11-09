"""Experimental Flask endpoint for LLM-assisted financial scenario exploration.

This project does not implement or validate tax calculations independently.
Do not use generated figures as professional tax advice.
"""
import json
import os

from flask import Flask, jsonify, request
from google import genai

app = Flask(__name__)

PROMPT_PADRAO = """
Você recebe dados financeiros em JSON para uma demonstração experimental.
Responda apenas com JSON válido, sem blocos Markdown.
Não afirme ter executado ARIMA ou cálculos fiscais determinísticos.
Não invente precisão ou certeza: sinalize hipóteses e dados ausentes.
Produza uma análise exploratória, não aconselhamento tributário.
Inclua os campos: companyId, year, metodo, observacoes, regimes e recomendado.
Use metodo = "llm:gemini-prototipo". Caso não possa comparar os regimes
com segurança, use recomendado = null e explique em observacoes.
"""

@app.post("/chat")
def chat():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict) or not dados:
        return jsonify({"error": "Envie um objeto JSON não vazio."}), 400

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return jsonify({"error": "Servidor sem GOOGLE_API_KEY configurada."}), 503

    try:
        client = genai.Client(api_key=api_key)
        resposta = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=f"{PROMPT_PADRAO}\n\nEntrada:\n{json.dumps(dados, ensure_ascii=False)}",
        )
        texto = (resposta.text or "").strip()
        resultado = json.loads(texto)
        if not isinstance(resultado, dict):
            return jsonify({"error": "O modelo não retornou um objeto JSON."}), 502
        return jsonify(resultado)
    except json.JSONDecodeError:
        return jsonify({"error": "O modelo não retornou JSON válido."}), 502
    except Exception:
        app.logger.exception("Falha ao processar solicitação de IA")
        return jsonify({"error": "Falha ao processar solicitação."}), 502


if __name__ == "__main__":
    app.run(debug=False)
