import jwt, string, secrets, bcrypt
from datetime import datetime
from app import app, db, secret
from app.wallet.model import Wallet

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    role = db.Column(db.String, nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)
    profile = db.relationship("Profile", uselist=False)
    wallet = db.relationship("Wallet", uselist=False)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        self.updated_at = db.func.now()
        db.session.commit()
    
    def delete(self):
        self.is_deleted = True
        self.update()
    
    @staticmethod
    def generate_password():
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(10))
        return password
    
    def hash_password(self):
        self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def generate_token(self):
        payload = {
            'exp': app.config.get('JWT_REFRESH_TOKEN_EXPIRES'),
            'iat': datetime.utcnow(),
            'sub': self.id,
            'role': self.role
        }
        return jwt.encode(payload, secret, algorithm='HS256')
    
    def update_password(self, old_password, new_password):
        if self.is_verified(old_password):
            self.password = new_password
            self.hash_password()
            self.update()
            return True
        return False
    
    def reset_password(self, new_password):
        self.password = new_password
        self.hash_password()
        self.update()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_by_email(self, email):
        return User.query.filter(User.email==email, User.is_deleted==False).first()
    
    @classmethod
    def create(cls, email, password, role):
        user = cls(email=email, password=password, role=role)
        user.hash_password()
        user.save()
        return user