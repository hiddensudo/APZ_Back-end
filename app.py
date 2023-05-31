from flask import Flask, render_template
from db import init_db
from my_jwt import secret_key
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = secret_key
app.secret_key = secret_key
mongo = init_db(app)
jwt = JWTManager(app)
CORS(app)

from routes.user_route import *
from routes.admin_route import *
from routes.building_routes import *
from routes.goods_route import *
from routes.order_route import *
from routes.day_analytics_route import *
from routes.month_analytics_route import *

if __name__ == '__main__':
    app.run()
