import json


def content_from_file(filename):
    content_file = open(filename, "r")
    content = content_file.read()
    return content


def json_from_file(filename):
    json_file = open(filename, "r")
    content = json.load(json_file)
    return content


def delete_related_obj(base_object):
    for relationship in base_object._meta.related_objects:
        model = relationship.related_model
        query_filter = {
            relationship.remote_field.name: base_object,
        }

        if relationship.one_to_many or relationship.one_to_one:
            for related_object in model.objects.filter(**query_filter).all():
                delete_related_obj(related_object)
                related_object.delete()
