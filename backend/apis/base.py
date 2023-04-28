class GenericDAO:
    def __init_subclass__(cls, /, target_schema, target_document):
        cls.schema = target_schema()
        cls.target_document = target_document

        target_document.dump = lambda self: cls.schema.dump(self)

    @classmethod
    def get_all(cls):
        documents = cls.target_document.objects()
        return cls.schema.dump(documents, many=True)

    @classmethod
    def get_by_id(cls, id):
        return cls.target_document.objects.get(id=id)

    @classmethod
    def create(cls, data):
        document = cls.target_document(**data)
        document.save()
        return cls.schema.dump(document)

    @classmethod
    def update(cls, id, data):
        document = cls.target_document.objects.get(id=id)
        document.update(**data)
        document.reload()
        return cls.schema.dump(document)

    @classmethod
    def delete(cls, id):
        document = cls.target_document.objects.get(id=id)
        document.delete()
