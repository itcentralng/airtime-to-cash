from flask import Blueprint, request, g
from app.route_guard import auth_required

from app.airtime.model import *
from app.airtime.schema import *

bp = Blueprint('airtime', __name__)

@bp.post('/airtime')
@auth_required()
def create_airtime():
    data = request.json
    wallet = Wallet.get_by_user_id(user_id=g.user.id)
    if data.get('type') != 'sell' and wallet.amount >= data.get("unit"):
        wallet.debit(data.get("unit"))
        if data.get("type") == "indirect":
            data['unit'] = data.get("unit")+data.get("unit")*0.1
    elif data.get('type') == 'direct':
        return {"status":"failed", "message":"Insufficient Funds"}
    airtime = Airtime.create(g.user.id, data.get('provider'), data.get("phone"), data.get("unit"), data.get("type"))
    return AirtimeSchema().dump(airtime), 201

@bp.get('/airtime/pending/<provider>')
@auth_required()
def get_pending_airtimes_by_provider(provider):
    airtimes = Airtime.get_pending_by_provider(provider)
    if not airtimes:
        return {'status':'failed', 'message': 'No pending numbers, try later'}, 404
    return AirtimeSchema(many=True).dump(airtimes), 200

@bp.get('/airtime/history')
@auth_required()
def get_airtime_history():
    airtimes = Airtime.get_by_user_id(g.user.id)
    return AirtimeSchema(many=True).dump(airtimes), 200