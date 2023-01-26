from app import db

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey("wallet.id"))
    amount = db.Column(db.Integer)
    type = db.Column(db.String, default='credit')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        self.updated_at = db.func.now()
        db.session.commit()
    
    def delete(self):
        self.is_deleted = True
        self.updated_at = db.func.now()
        db.session.commit()

    @classmethod
    def get_by_wallet_id(cls, wallet_id):
        return cls.query.filter_by(wallet_id=wallet_id, is_deleted=False).all()
    
    @classmethod
    def get_by_id(cls):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def create(cls, wallet_id, amount, type):
        transaction = cls(wallet_id=wallet_id, amount=amount, type=type)
        transaction.save()
        return transaction