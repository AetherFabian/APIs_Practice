from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from flask_pymongo import pymongo
from pymongo import response
import db_config as database

app = Flask(__name__)
api = Api(app)

post_students_args = reqparse.RequestParser()

post_students_args.add_argument("id", type=int, help="ERROR id value needs to be an integer", required = True)
post_students_args.add_argument("first_name", type=str, help="ERROR first_name is required", required = True)
post_students_args.add_argument("last_name", type=str, help="ERROR last_name is required", required = True)
post_students_args.add_argument("image", type=str, help="ERROR you need to add the image url", required = True)
post_students_args.add_argument("group", type=str, required = False)
post_students_args.add_argument("career", type=str, required = False)

class Test(Resource):

    def get(self):
        database.db.students.find()
        return jsonify({'message': 'You are connected to the database'})

class Student(Resource):

    def get(self,id):
        response = database.db.students.find_one({"id": id})
        del response['_id']
        return jsonify(response)

class Students(Resource):

    def get(self):
        response = list(database.db.students.find())
        students = []
        for student in response:
            del student['_id']
            students.append(student)
        return jsonify(students)

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


    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass

    def abort_if_id_exists(self, id):
        if database.db.students.find_one({'id': id}):
            abort(jsonify({'status': '406', 'error': f'Student with id: {id} already exists'}))

api.add_resource(Test, '/test/')
api.add_resource(Students, '/students/')
api.add_resource(Student, '/students/<int:id>/')

if __name__ == '__main__':
    app.run(load_dotenv=True, port=8080)