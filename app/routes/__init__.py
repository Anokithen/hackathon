from app.routes.auth_routes import auth_bp
from app.routes.customers_routes import customer_bp
from app.routes.user_routes import user_bp


def register_blueprints(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(auth_bp)

