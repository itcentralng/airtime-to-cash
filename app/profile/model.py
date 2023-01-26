from app import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    provider = db.Column(db.String, default='MTN')
    image = db.Column(db.String, default='avatar.png')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, name=None, phone=None, provider=None, image=None):
        self.name = name or self.name
        self.phone = phone or self.phone
        self.provider = provider or self.provider
        self.image = image or self.image
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
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id, is_deleted=False).first()
    
    @classmethod
    def create(cls, user_id, name, phone, provider, image=None):
        profile = cls(user_id=user_id, name=name, phone=phone, provider=provider, image=image)
        profile.save()
        return profile