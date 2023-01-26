from app import ma
from app.transaction.model import *

class TransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transaction
        exclude = ('is_deleted',)