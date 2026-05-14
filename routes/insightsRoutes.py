from flask import Blueprint, jsonify, g
from middlewares.authRequired import auth_required
from db.database import profiles_collection
from services.ia_insights_service import gerar_insight_gemini

insights_bp = Blueprint("insights", __name__)

@insights_bp.route("/insights/areas-em-alta", methods=["GET"])
@auth_required(["student"])
def get_areas_em_alta():
    profile = profiles_collection.find_one({"user_id": g.current_user_id})
    if not profile:
        return jsonify({"error": "Perfil não encontrado."}), 404

    curso = profile.get("curso", "")
    interesses = profile.get("interesses", [])
    habilidades = profile.get("habilidades", [])
    materias = profile.get("materiasConcluidas", "")
    try:
        resposta = gerar_insight_gemini("areas", curso, interesses, habilidades, materias)
        return jsonify({"insight": resposta})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Erro ao gerar insight. Tente novamente mais tarde."}), 500


@insights_bp.route("/insights/carreira", methods=["GET"])
@auth_required(["student"])
def get_carreira_insight():
    profile = profiles_collection.find_one({"user_id": g.current_user_id})
    if not profile:
        return jsonify({"error": "Perfil não encontrado."}), 404

    curso = profile.get("curso", "")
    interesses = profile.get("interesses", [])
    habilidades = profile.get("habilidades", [])
    materias = profile.get("materiasConcluidas", "")

    try:
        resposta = gerar_insight_gemini("carreira", curso, interesses, habilidades, materias)
        return jsonify({"insight": resposta})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Erro ao gerar insight. Tente novamente mais tarde."}), 500
