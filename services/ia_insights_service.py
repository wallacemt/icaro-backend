import json
import re
import google.generativeai as genai
from config.config import GEMINIAI_KEY
from config.config import GEMINIAI_MODEL


genai.configure(api_key=GEMINIAI_KEY)
_model = genai.GenerativeModel(GEMINIAI_MODEL)


def gerar_insight_gemini(tipo_insight, curso, interesses, habilidades, materias_concluidas):
    contexto = (
        "Você é uma IA que atua dentro do sistema Ícaro, uma plataforma inteligente que conecta alunos a oportunidades de estágio. "
        "Com base no perfil do aluno, gere um insight em formato JSON que será usado para construir um gráfico no frontend. "
        "O JSON deve conter uma lista de objetos com os seguintes campos:\n"
        "- 'label': o nome da área ou carreira\n"
        "- 'value': um número representando relevância ou tendência (porcentagem ou peso)\n"
        "- 'description': uma breve explicação de cada item\n\n"
        "Esse conteúdo será mostrado visualmente em um gráfico com informações adicionais para o aluno."
    )
    if tipo_insight == "areas":
        objetivo = "Gere um gráfico de áreas de atuação em alta para esse o curso desse aluno."
    elif tipo_insight == "carreira":
        objetivo = "Gere um gráfico de caminhos de carreira compatíveis com esse perfil. Considere as tendências atuais do mercado de trabalho e as competências informadas. "
    else:
        raise ValueError("Tipo de insight inválido.")

    prompt = (
        f"{contexto}\n\n{objetivo}\n\n"
        f"Curso: {curso}\n"
        f"Materias Concluidas: {', '.join(materias_concluidas)}\n"
        f"Interesses: {', '.join(interesses)}\n"
        f"Habilidades: {', '.join(habilidades)}"
    )

    response = _model.generate_content(prompt)
    raw_text = response.text

    try:
        cleaned = re.sub(r"```json|```", "", raw_text).strip()
        return json.loads(cleaned)
    except (json.JSONDecodeError, AttributeError):
        return {"error": "Erro ao processar resposta da IA."}


def calcular_progresso_curso_gemini(curso, materias_concluidas):
    prompt = (
        "Você é uma IA que atua no sistema Ícaro, que conecta alunos a oportunidades de estágio. "
        "Com base no curso do aluno e nas disciplinas que ele já concluiu, estime a porcentagem de conclusão do curso. "
        "Considere o currículo típico para esse curso no Brasil. "
        "Responda apenas com um JSON válido com o seguinte formato:\n\n"
        "{ \"porcentCompleted\": <número entre 0 e 100> }"
        f"\n\nCurso: {curso}\nMatérias concluídas: {materias_concluidas}"
    )

    response = _model.generate_content(prompt)
    raw_text = response.text

    try:
        cleaned = re.sub(r"```json|```", "", raw_text).strip()
        return json.loads(cleaned)
    except (json.JSONDecodeError, AttributeError):
        return {"error": "Erro ao processar resposta da IA."}
