from app import ma
from app.profile.model import *

class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        exclude = ('is_deleted',)