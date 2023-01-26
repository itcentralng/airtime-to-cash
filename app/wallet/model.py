from app import db

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    account_number = db.Column(db.String, nullable=False)
    account_name = db.Column(db.String, nullable=False)
    bank = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, account_number=None, account_name=None, bank=None):
        self.account_number = account_number or self.account_number
        self.account_name = account_name or self.account_name
        self.bank = bank or self.bank
        self.updated_at = db.func.now()
        db.session.commit()
    
    def delete(self):
        self.is_deleted = True
        self.updated_at = db.func.now()
        db.session.commit()
    
    def credit(self, amount):
        self.amount += amount
        self.update()
    
    def debit(self, amount):
        self.amount -= amount
        self.update()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id, is_deleted=False).first()
    
    @classmethod
    def create(cls, user_id, account_number, account_name, bank):
        wallet = cls(user_id=user_id, account_number=account_number, account_name=account_name, bank=bank)
        wallet.save()
        return wallet