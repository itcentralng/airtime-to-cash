from flask import Blueprint
from app.route_guard import auth_required

from app.wallet.model import *
from app.wallet.schema import *

bp = Blueprint('wallet', __name__)

@bp.post('/wallet')
@auth_required()
def create_wallet():
    wallet = Wallet.create()
    return WalletSchema().dump(wallet), 201

@bp.get('/wallet/<int:id>')
@auth_required()
def get_wallet(id):
    wallet = Wallet.get_by_id(id)
    if wallet is None:
        return {'message': 'Wallet not found'}, 404
    return WalletSchema().dump(wallet), 200

@bp.patch('/wallet/<int:id>')
@auth_required()
def update_wallet(id):
    wallet = Wallet.get_by_id(id)
    if wallet is None:
        return {'message': 'Wallet not found'}, 404
    wallet.update()
    return WalletSchema().dump(wallet), 200

@bp.delete('/wallet/<int:id>')
@auth_required()
def delete_wallet(id):
    wallet = Wallet.get_by_id(id)
    if wallet is None:
        return {'message': 'Wallet not found'}, 404
    wallet.delete()
    return {'message': 'Wallet deleted successfully'}, 200

@bp.get('/wallets')
@auth_required()
def get_wallets():
    wallets = Wallet.get_all()
    return WalletSchema(many=True).dump(wallets), 200