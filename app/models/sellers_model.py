from app.extensions import db


class Seller(db.Model):
    __tablename__ = "sellers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    shop_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)

    user = db.relationship("User", back_populates="seller")
    products = db.relationship("Product", back_populates="seller", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "shop_name": self.shop_name,
            "phone": self.phone,
            "address": self.address,
        }
