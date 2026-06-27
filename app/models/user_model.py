from app.extensions import db
from app.utils import utc_now
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum

class RoleEnum(Enum):
    admin = "admin"
    customer = "customer"
    seller = "seller"

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(120),nullable=False,unique=True)
    password = db.Column(db.String(255),nullable=False)
    role = db.Column(db.Enum(RoleEnum),nullable=False,default=RoleEnum.customer)
    is_active = db.Column(db.Boolean,default=True,nullable=False)
    created_at = db.Column(db.DateTime,default=utc_now)


    def set_password(self, password):
        self.password = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password, password)


    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role.value if self.role else None,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


