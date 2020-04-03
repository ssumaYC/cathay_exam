from flask import Response, request
from database.models import RentingHouse
from flask_restful import Resource
from .toolbox import pretty_json, get_qs_dict


class RentingHouseApi(Resource):
    def get(self, post_id):
        r_house = RentingHouse.objects.get_or_404(post_id=post_id).to_json()
        r_house = pretty_json(r_house)
        return Response(r_house, mimetype="application/json", status=200)


class RentingHousesApi(Resource):
    def get(self):
        try:
            qs_dict = get_qs_dict(request)
            query = qs_dict_to_mongo_query(qs_dict)
            r_houses = RentingHouse.objects(__raw__=query)
            num_data = RentingHouse.objects(__raw__=query).count()
            r_houses = [r_house.to_json() for r_house in r_houses]
            data = {"success": True, "num_data": num_data, "data": r_houses}
        except Exception as e:
            #TODO handle the exception
            data = {"success": False}
        data = pretty_json(data)
        return Response(data, mimetype="application/json", status=200)


def qs_dict_to_mongo_query(qs_dict):
    qs_dict = {k: v[0] for k, v in qs_dict.items()}
    query = {
        "region": qs_dict.get("region"),
        "tel": qs_dict.get("phone"),
        "poster_gender": qs_dict.get("poster-gender"),
        "gender_acception": map_gender_accept(qs_dict.get("gender-accept")),
        "poster_identity": map_is_owner(qs_dict.get("is-owner")),
        "poster_title": map_poster_lname(qs_dict.get("poster-lname")),
    }
    query = {k: v for k, v in query.items() if v is not None}
    return query


def map_gender_accept(v):
    if v is not None:
        v_map = {
            "male": {"$in": ["male", "both"]},
            "male-only": "male",
            "female": {"$in": ["female", "both"]},
            "female-only": "female",
        }
        value = v_map.get(v, None)
        return value
    else:
        return None


def map_is_owner(v):
    v_map = {"1": "owner", "0": {"$ne": "owner"}}
    value = v_map.get(v, None)
    return value


def map_poster_lname(v):
    if v is not None:
        return {"$regex": f"^{v}", "$options": "i"}
    else:
        return None
