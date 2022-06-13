import os

from flask import Flask
from flask_migrate import Migrate
from routes import order_blueprint
from models import db, init_app

os.makedirs("database", exist_ok=True)

app = Flask(__name__)

app.config["SECRET_KEY"] = 'Ym3iRUN0aGlhDg6hSdR_vK'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./database/order.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.register_blueprint(order_blueprint)

init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5003)


