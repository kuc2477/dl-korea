from .models import User
from ..extensions import db
from flask.ext.restful import (
    Resource,
    reqparse,
)


class UserResource(Resource):
        def get(self, id):
            user = User.query.get_or_404(id)
            return user.serialized

        def delete(self, id):
            user = User.query.get(id)
            db.session.delete(user)
            return '', 204

        def put(self, id):
            parser = reqparse.RequestParser()
            parser.add_argument('firstname')
            parser.add_argument('lastname')
            args = parser.parse_args()

            user = User.query.get_or_404(id)
            user.firstname = args['firstname']
            user.lastname = args['lastname']
            db.session.commit()
            return user.serialized
