from flask import Blueprint, request
from app.route_guard import auth_required

from app.profile.model import *
from app.profile.schema import *

bp = Blueprint('profile', __name__)

@bp.patch('/profile/<int:user_id>')
@auth_required()
def update_profile(user_id):
    data = request.json
    profile = Profile.get_by_user_id(user_id)
    if profile is None:
        return {'message': 'Profile not found'}, 404
    profile.update(name=data.get('name'), phone=data.get('phone'), provider=data.get('provider'), image=data.get('image'))
    return ProfileSchema().dump(profile), 200