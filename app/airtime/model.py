from app import db
from helpers.airtime_helper import send_airtime
from app.wallet.model import Wallet

class Airtime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    phone_number = db.Column(db.String)
    provider = db.Column(db.String, default='MTN')
    unit = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, default='pending')
    type = db.Column(db.String, default='direct')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, status):
        self.status = status
        self.updated_at = db.func.now()
        db.session.commit()
    
    def delete(self):
        self.is_deleted = True
        self.updated_at = db.func.now()
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_pending_by_phone_number(cls, phone_number):
        return cls.query.filter_by(phone_number=phone_number, status="pending", is_deleted=False).first()
    
    @classmethod
    def get_pending_by_provider(cls, provider):
        return cls.query.filter_by(provider=provider, status="pending", is_deleted=False).all()
    
    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id, is_deleted=False).all()
    
    @classmethod
    def create(cls, user_id, provider, phone_number, unit, type):
        airtime = cls(user_id=user_id, provider=provider, phone_number=phone_number, unit=unit, type=type)
        airtime.save()
        # send airtime if type is 'direct'
        if airtime.type == 'direct':
            send_airtime(unit, phone_number)
            airtime.update(status='complete')
        elif airtime.type == 'sell':
            old_airtime = Airtime.get_pending_by_phone_number(phone_number)
            old_airtime.update(status='complete')
            airtime.update(status='complete')
        return airtime