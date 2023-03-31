from flask_restx import Namespace, Resource, fields
import mongoengine as me
import marshmallow_mongoengine as ma

me.connect("pets", host="localhost", port=27017)


class Dog(me.Document):
    name = me.StringField(primary_key=True)
    toys = me.ListField(me.StringField())


class DogSchema(ma.ModelSchema):
    class Meta:
        model = Dog


class DogDAO:
    def __init__(self):
        self.schema = DogSchema()

    def get_all(self):
        dogs = Dog.objects()
        return self.schema.dump(dogs, many=True)

    def get_by_id(self, id):
        return Dog.objects.get(id=id)

    def create(self, data):
        dog = Dog(**data)
        dog.save()
        return self.schema.dump(dog)

    def update(self, id, data):
        dog = Dog.objects.get(id=id)
        dog.update(**data)
        dog.reload()
        return self.schema.dump(dog)

    def delete(self, id):
        dog = Dog.objects.get(id=id)
        dog.delete()


api = Namespace("dogs", description="Dogs related operations")

dog = api.model(
    "Dog",
    {
        "name": fields.String(required=True, description="The dog name"),
        "toys": fields.List(fields.String(), required=False, description="The dogs toys"),
    },
)

dog_dao = DogDAO()


@api.route("/")
class DogListResource(Resource):
    @api.doc("list_dogs")
    @api.marshal_list_with(dog)
    def get(self):
        return dog_dao.get_all(), 200

    @api.doc("post_dog")
    @api.expect(dog)
    @api.marshal_with(dog, code=201)
    def post(self):
        data = api.payload
        return dog_dao.create(data), 201


@api.route("/<string:id>")
@api.param("id", "The dog identifier")
@api.response(404, "Dog not found")
class DogResource(Resource):
    @api.doc("get_dog")
    @api.marshal_with(dog)
    def get(self, id):
        return dog_dao.get_by_id(id)

    @api.doc("put_dog")
    @api.marshal_with(dog)
    def put(self, id):
        data = api.payload()
        return dog_dao.update(id, data)

    @api.doc("delete_dog")
    @api.response(204, "Dog deleted")
    def delete(self, id):
        dog_dao.delete(id)
        return "", 204
