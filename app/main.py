'''import libraries of flask framework to work on an API'''
from unittest.mock import patch
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from flask_cors import CORS
import app.db_config as database

'''Identify resources as variables fo the application'''
app = Flask(__name__)
api = Api(app)
CORS(app)

'''provide variable to request parser'''
post_students_args = reqparse.RequestParser()

'''define the resources with some requests'''
post_students_args.add_argument("id", type=int, help="ERROR id value needs to be an integer", required = True)
post_students_args.add_argument("first_name", type=str, help="ERROR first_name is required", required = True)
post_students_args.add_argument("last_name", type=str, help="ERROR last_name is required", required = True)
post_students_args.add_argument("image", type=str, help="ERROR you need to add the image url", required = True)
post_students_args.add_argument("group", type=str, required = False)
post_students_args.add_argument("career", type=str, required = False)

'''provide variable to request parser'''
patch_students_args = reqparse.RequestParser()

'''define the arguments with no required'''
patch_students_args.add_argument("id", type=int, help="ERROR id value needs to be an integer", required = False)
patch_students_args.add_argument("first_name", type=str, help="ERROR first_name is required", required = False)
patch_students_args.add_argument("last_name", type=str, help="ERROR last_name is required", required = False)
patch_students_args.add_argument("image", type=str, help="ERROR you need to add the image url", required = False)
patch_students_args.add_argument("group", type=str, required = False)
patch_students_args.add_argument("career", type=str, required = False)

'''Try if we connect to the database'''
class Test(Resource):

    def get(self):
        database.db.students.find()
        return jsonify({'message': 'You are connected to the database'})

'''Use methods of get students, post students, put students, patch students and delete students'''
class Student(Resource):

    '''Get student by id that we created'''
    def get(self,id):
        response = database.db.students.find_one({"id": id})
        del response['_id']
        return jsonify(response)

    '''post arguments that will be insert on the database as Json and if 
    the id already exists, it will return an error'''
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

    '''put arguments overwritten the existed student on the database as Json
    and if it doesn't exist, it abort the operation'''
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

    '''patch can overwritten specific data on a existed student by id on the database as Json
    and if it doesn't exist, it abort the operation'''
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

    '''delete student by id'''
    def delete(self, id):
        student = self.abort_if_not_exists(id)
        database.db.students.delete_one({'id': id})
        del student['_id']
        return jsonify({'deleted': student})

    '''abort operation if the id exists and shows an error message'''
    def abort_if_id_exists(self, id):
        if database.db.students.find_one({'id': id}):
            abort(jsonify({'error': {'406', f'Student with id: {id} already exists'}}))

    '''abort operation if the student doesn't exist and shows an error message'''
    def abort_if_not_exists(self, id):
        student = database.db.students.find_one({'id': id})
        if not student:
            abort(jsonify({'error': {'404': f'Student with id: {id} not found'}}))
        else:
            return student

'''class students as a resource'''
class Students(Resource):

    '''get all students in the database'''
    def get(self):
        response = list(database.db.students.find())
        students = []
        for student in response:
            del student['_id']
            students.append(student)
        return jsonify(students)


'''add the resources to the api(endpoints)'''
api.add_resource(Test, '/test/')
api.add_resource(Students, '/students/')
api.add_resource(Student, '/student/', '/student/<int:id>/')

'''run the app with a port and take the environment'''
if __name__ == '__main__':
    app.run(load_dotenv=True, port=8080)