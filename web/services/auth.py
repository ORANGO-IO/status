from functools import wraps
from flask import request, jsonify
from web.models import Credential

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "").strip()

        if not token:
            return jsonify(error="Token de autenticação ausente"), 401

        token_record = Credential.query.filter_by(secret=token, role="token", system="api").first()
        if not token_record:
            return jsonify(error="Token inválido ou não autorizado"), 403

        return f(*args, **kwargs)

    return decorated_function