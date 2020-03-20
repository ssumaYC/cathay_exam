from flask_mongoengine import MongoEngine
import json


db = MongoEngine()


class RentingHouse(db.Document):
    meta = {
        'collection': 'renting_houses'
    }
    source = db.StringField(required=True)
    post_id = db.StringField(required=True, unique=True)
    poster_title = db.StringField(required=True)
    poster_gender = db.StringField(required=True)
    poster_identity = db.StringField(required=True)
    tel = db.StringField(required=True)
    house_type = db.StringField(required=True)
    room_type = db.StringField(required=True)
    gender_acception = db.StringField(required=True)
    house_description = db.StringField(required=True)
    region = db.StringField()

    def to_json(self):
        json_text = super().to_json()
        d = json.loads(json_text)
        del d['_id']
        return d
