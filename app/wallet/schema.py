from app import ma
from app.wallet.model import *

class WalletSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Wallet
        exclude = ('is_deleted',)