#!/usr/bin/python3
"""A view for State objects that handles all default RESTFul API actions
"""
from models import storage
from models.state import State
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request


@app_views.route("/states", strict_slashes=False)
def all_states():
    """ Retrieves the list of all State objects """
    li = []
    all_state = storage.all(State)
    for key in all_state:
            li.append(all_state[key].to_dict())
    return jsonify(li)


@app_views.route("/states/<state_id>", strict_slashes=False)
def get_state(state_id):
    """ Retrieves a 'State' object """
    all_objs = storage.all(State)
    for key in all_objs:
        if all_objs[key].id == state_id:
            return jsonify(all_objs[key].to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_task(state_id):
    ''' Deletes a 'State' object '''
    all_objs = storage.all(State)
    for key in all_objs:
        if all_objs[key].id == state_id:
            storage.delete(all_objs[key])
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    ''' Creates a "State" object '''
    obj_di = request.get_json()
    if not obj_di:
        return make_response("Not a JSON", 400)
    elif 'name' not in obj_di:
        return make_response("Missing name", 400)
    st_obj = State(**obj_di)
    storage.new(st_obj)
    storage.save()
    return st_obj.to_dict(), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a State object """
    attrs = request.get_json(silent=True)
    if not attrs:
        return make_response("Not a JSON", 400)
    di = storage.all("State")
    ignored_keys = ["id", "created_at", "updated_at"]
    for obj in di:
        if di[obj].id == state_id:
            for key, value in attrs.items():
                if key not in ignored_keys:
                    setattr(di[obj], key, value)
            storage.save()
            return di[obj].to_dict(), 200
    abort(404)
