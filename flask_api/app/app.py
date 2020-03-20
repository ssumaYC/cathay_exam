from flask import Flask
from database.models import db
from resources.rentingHouse import RentingHouseApi, RentingHousesApi
from flask_restful import Api


app = Flask(__name__)
api = Api(app)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://mongo:27017/cathay_exam'
}
db.init_app(app)


api.add_resource(RentingHouseApi, '/rentingHouses/<post_id>')
api.add_resource(RentingHousesApi, '/rentingHouses')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
