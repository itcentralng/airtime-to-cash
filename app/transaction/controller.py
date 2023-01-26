from flask import Blueprint, request
from app.route_guard import auth_required

from app.transaction.model import *
from app.transaction.schema import *
from app.wallet.model import Wallet

bp = Blueprint('transaction', __name__)

@bp.post('/transaction')
@auth_required()
def create_transaction():
    data = request.json
    transaction = Transaction.create(data.get('wallet_id'), data.get('amount'), data.get('type'))
    wallet = Wallet.get_by_id(transaction.wallet_id)
    if transaction.type == 'credit':
        wallet.credit(transaction.amount)
    else:
        wallet.debit(transaction.amount)
    return TransactionSchema().dump(transaction), 201

@bp.get('/transaction/<int:id>')
@auth_required()
def get_transaction(id):
    transaction = Transaction.get_by_id(id)
    if transaction is None:
        return {'message': 'Transaction not found'}, 404
    return TransactionSchema().dump(transaction), 200

@bp.get('/transactions/<int:wallet_id>')
@auth_required()
def get_transactions_by_wallet_id(wallet_id):
    transactions = Transaction.get_by_wallet_id(wallet_id)
    return TransactionSchema(many=True).dump(transactions), 200