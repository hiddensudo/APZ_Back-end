from flask_pymongo import PyMongo


def init_db(app):
    app.config[
        "MONGO_URI"] = "mongodb+srv://hidden:7285Dudahidden028@cluster.v4cpdkt.mongodb.net/apz_database?retryWrites=true&w=majority"
    mongo = PyMongo(app)
    return mongo
