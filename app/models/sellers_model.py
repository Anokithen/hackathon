from app.extensions import db


class Seller(db.Model):
    __tablename__ = "sellers"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id =db.Column(db.Integer, db.Foreginkey('users.id'))
    shop_name = db.Column(db.String)
    phone = db.Column(db.String,min(10))
    address =db.Column(db.string)



    def to_dict(self):
        return{
            "id":self.id
        }