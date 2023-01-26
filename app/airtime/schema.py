from app import ma
from app.airtime.model import *

class AirtimeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Airtime
        exclude = ('is_deleted',)