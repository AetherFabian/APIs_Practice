from unittest.mock import patch
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from flask_cors import CORS
import app.db_config as database

app = Flask(__name__)
api = Api(app)
CORS(app)

post_students_args = reqparse.RequestParser()

post_students_args.add_argument("id", type=int, help="ERROR id value needs to be an integer", required = True)
post_students_args.add_argument("first_name", type=str, help="ERROR first_name is required", required = True)
post_students_args.add_argument("last_name", type=str, help="ERROR last_name is required", required = True)
post_students_args.add_argument("image", type=str, help="ERROR you need to add the image url", required = True)
post_students_args.add_argument("group", type=str, required = False)
post_students_args.add_argument("career", type=str, required = False)

patch_students_args = reqparse.RequestParser()

patch_students_args.add_argument("id", type=int, help="ERROR id value needs to be an integer", required = False)
patch_students_args.add_argument("first_name", type=str, help="ERROR first_name is required", required = False)
patch_students_args.add_argument("last_name", type=str, help="ERROR last_name is required", required = False)
patch_students_args.add_argument("image", type=str, help="ERROR you need to add the image url", required = False)
patch_students_args.add_argument("group", type=str, required = False)
patch_students_args.add_argument("career", type=str, required = False)


class Test(Resource):

    def get(self):
        database.db.students.find()
        return jsonify({'message': 'You are connected to the database'})

class Student(Resource):

    def get(self,id):
        response = database.db.students.find_one({"id": id})
        del response['_id']
        return jsonify(response)

    def post(self):
        args = post_students_args.parse_args()
        self.abort_if_id_exists(args['id'])
        database.db.students.insert_one({
            'id': args['id'],
            'first_name': args['first_name'],
            'last_name': args['last_name'],
            'image': args['image'],
            'group': args['group'],
            'career': args['career']
        })
        return jsonify(args)


    def put(self, id):
        args = post_students_args.parse_args()
        self.abort_if_not_exists(id)
        database.db.students.update_one(
            {'id': id},
            {'$set': {
                'id': args['id'],
                'first_name': args['first_name'],
                'last_name': args['last_name'],
                'image': args['image'],
                'group': args['group'],
                'career': args['career'],
            }}
        )
        return jsonify(args)

    def patch(self, id):
        student = self.abort_if_not_exists(id)
        args = patch_students_args.parse_args()
        database.db.students.update_one(
            {'id': id},
            {'$set': {
                'id': args['id'] or student['id'],
                'first_name': args['first_name'] or student['first_name'],
                'last_name': args['last_name'] or student['last_name'],
                'image': args['image'] or student['image'],
                'group': args['group'] or student['group'],
                'career': args['career'] or student['career'],
            }}
        )
        student = self.abort_if_not_exists(id)
        del student['_id']
        return jsonify(student)

    def delete(self, id):
        student = self.abort_if_not_exists(id)
        database.db.students.delete_one({'id': id})
        del student['_id']
        return jsonify({'deleted': student})

    def abort_if_id_exists(self, id):
        if database.db.students.find_one({'id': id}):
            abort(jsonify({'error': {'406', f'Student with id: {id} already exists'}}))

    def abort_if_not_exists(self, id):
        student = database.db.students.find_one({'id': id})
        if not student:
            abort(jsonify({'error': {'404': f'Student with id: {id} not found'}}))
        else:
            return student

class Students(Resource):

    def get(self):
        response = list(database.db.students.find())
        students = []
        for student in response:
            del student['_id']
            students.append(student)
        return jsonify(students)



api.add_resource(Test, '/test/')
api.add_resource(Students, '/students/')
api.add_resource(Student, '/student/', '/student/<int:id>/')

if __name__ == '__main__':
    app.run(load_dotenv=True, port=8080)