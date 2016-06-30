from flask import request
from flask.ext.restful import Resource
from .models import User
from .forms import UserUpdateForm
from ..extensions import db


class UserResource(Resource):
        def get(self, id):
            user = User.query.get_or_404(id)
            return user.serialized

        def delete(self, id):
            user = User.query.get(id)
            db.session.delete(user)
            db.session.commit()
            return '', 204

        def put(self, id):
            form = UserUpdateForm(**request.json)
            form.validate()

            user = User.query.get_or_404(id)
            user.firstname = form.firstname.data
            user.lastname = form.lastname.data
            db.session.commit()

            return user.serialized
