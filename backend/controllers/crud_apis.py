from unittest import result

from flask_restful import Resource
from flask import request, jsonify,make_response
from flask_security import utils,auth_token_required,roles_required

from controllers.user_datastore import user_datastore,db
from controllers.models import *

class CategoryAPI(Resource):
    def get(self, category_id=None):
        if category_id:
            category = Category.query.get(category_id)
            if not category:
                result = {
                    'message': 'Category not found'
                }
                return make_response(jsonify(result), 404)
            result = {
                'id': category.id,
                'name': category.name,
                'description': category.description
            }
            return make_response(jsonify(result), 200)
        else:
            categories = Category.query.all()
            result = []
            for category in categories:
                result.append({
                    'id': category.id,
                    'name': category.name,
                    'description': category.description
                })
            return make_response(jsonify(result), 200)

    @roles_required('admin')
    def post(self):
          data=request.get_json()
          if not data:
              result={
                  'message':'Category data is required'
              }
              return make_response(jsonify(result),400)
          
          name=data.get('name')
          description=data.get('description')

          if not name:
              result={
                  'message':'Category name is required'
              }
              return make_response(jsonify(result),400)
          
          new_category=Category(name=name,description=description)
          db.session.add(new_category)
          db.session.commit()

          result={
                'message':'Category created successfully',
                'category':{
                    'id':new_category.id,
                    'name':new_category.name,
                    'description':new_category.description
                }
          }
          return make_response(jsonify(result),201)
    
    @auth_token_required
    @roles_required('admin')
    def put(self, category_id):
        category = Category.query.get(category_id)
        if not category:
            result = {
                'message': 'Category not found'
            }
            return make_response(jsonify(result), 404)

        data = request.get_json()
        if not data:
            result = {
                'message': 'Category data is required'
            }
            return make_response(jsonify(result), 400)

        name = data.get('name')
        description = data.get('description')

        if name:
            category.name = name
        if description:
            category.description = description

        db.session.commit()

        result = {
            'message': 'Category updated successfully',
            'category': {
                'id': category.id,
                'name': category.name,
                'description': category.description
            }
        }
        return make_response(jsonify(result), 200)
    
    @auth_token_required
    @roles_required('admin')
    def delete(self, category_id):
        category = Category.query.get(category_id)
        if not category:
            result = {
                'message': 'Category not found'
            }
            return make_response(jsonify(result), 404)

        db.session.delete(category)
        db.session.commit()

        result = {
            'message': 'Category deleted successfully'
        }
        return make_response(jsonify(result), 200)
        