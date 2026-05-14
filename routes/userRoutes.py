from flask import Blueprint, request, jsonify, g
from middlewares.authRequired import auth_required
from db.database import users_collection, profiles_collection
from services.ia_insights_service import calcular_progresso_curso_gemini
from bson import ObjectId
from db.models import ProfileUpdate
from fastapi.encoders import jsonable_encoder
from pymongo import ReturnDocument
user_bp = Blueprint("user", __name__)
@user_bp.route('/user', methods=['GET'])
@auth_required(["student", "teacher"])
def get_me():
    user = users_collection.find_one({"_id": ObjectId(g.current_user_id)})

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    profile = profiles_collection.find_one({"user_id": g.current_user_id})

    user["_id"] = str(user["_id"])
    if profile:
        profile["_id"] = str(profile["_id"])
        profile["curso"] = profile["curso"].replace("_", " ").capitalize()
        profile["porcentagem_conclusao"] = calcular_progresso_curso_gemini(profile["curso"], profile["numeroMateriasConcluidas"])
        user["profile"] = profile
    else:
        user["profile"] = None
    adminName = user.get("name")
    return jsonify({
        "id": str(user["_id"]),
        "nome": user["nome"],
        "adminName": adminName if adminName else None,
        "email": user["email"],
        "role": user["role"],
        "acessAt": user["acessAt"],
        "isFullProfile": user.get("isFullProfile", False),
        "profile": user["profile"]
    }), 200


@user_bp.route("/user/profile", methods=["POST"])
@auth_required(["student"])
def create_or_update_profile():
    try:
        profile_data = ProfileUpdate(**request.json)
        clean_data = jsonable_encoder(profile_data)

        profiles_collection.update_one(
            {"user_id": g.current_user_id},
            {"$set": {**clean_data, "user_id": g.current_user_id}},
            upsert=True
        )

        if "nome" in request.json:
            nome = request.json["nome"]
            res = users_collection.find_one_and_update(
                {"_id": ObjectId(g.current_user_id)},
                {"$set": {"nome": nome, "isFullProfile": True}},
                return_document=ReturnDocument.AFTER
            )

        return jsonify({"message": "Perfil atualizado com sucesso"}), 200
    except ValueError as e:
        return jsonify({"error": e.errors()}), 422
    except Exception:
        return jsonify({"error": "Erro interno. Tente novamente mais tarde."}), 500
