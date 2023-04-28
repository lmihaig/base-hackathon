from flask_restx import Namespace, Resource, fields
import mongoengine as me
import marshmallow_mongoengine as ma
from os import environ
from .base import GenericDAO

me.connect("pets", host=environ.get("MONGO_HOST", "localhost"), port=27017)


class Dog(me.Document):
    name = me.StringField(primary_key=True)
    toys = me.ListField(me.StringField())


class DogSchema(ma.ModelSchema):
    class Meta:
        model = Dog


class DogDAO(GenericDAO, target_schema = DogSchema, target_document = Dog):
    pass


api = Namespace("dogs", description="Dogs related operations")

dog = api.model(
    "Dog",
    {
        "name": fields.String(required=True, description="The dog name"),
        "toys": fields.List(fields.String(), required=False, description="The dogs toys"),
    },
)


@api.route("/")
class DogListResource(Resource):
    @api.doc("list_dogs")
    @api.marshal_list_with(dog)
    def get(self):
        return DogDAO.get_all(), 200

    @api.doc("post_dog")
    @api.expect(dog)
    @api.marshal_with(dog, code=201)
    def post(self):
        data = api.payload
        return DogDAO.create(data), 201


@api.route("/<string:id>")
@api.param("id", "The dog identifier")
@api.response(404, "Dog not found")
class DogResource(Resource):
    @api.doc("get_dog")
    @api.marshal_with(dog)
    def get(self, id):
        return DogDAO.get_by_id(id)

    @api.doc("put_dog")
    @api.marshal_with(dog)
    def put(self, id):
        data = api.payload()
        return DogDAO.update(id, data)

    @api.doc("delete_dog")
    @api.response(204, "Dog deleted")
    def delete(self, id):
        DogDAO.delete(id)
        return "", 204
