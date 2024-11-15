from flask import Flask, render_template, request, jsonify,Response
from web import send_slack_notification
from models import db, Module, TestCase
from create_db import create_db
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

DB_URL = os.getenv("DB_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def count_children(module):
    direct_children = Module.query.filter_by(parent_id=module.id).count()
    return direct_children

def build_tree(modules, parent_id=None):
    tree = []
    for module in modules:
        if module.parent_id == parent_id:
            child_count = count_children(module)
            display_name = f"{module.name} ({child_count})" if child_count > 0 else module.name
            children = build_tree(modules, module.id)
            tree.append({
                'id': module.id,
                'text': display_name, 
                'children': children
            })
    return tree

@app.route('/')
def index():
    modules = Module.query.all()
    tree = build_tree(modules)
    return render_template('index.html', tree=tree)

#--------------------Modules---------------#
##This module below is used to get the module details
###When you click on the module name on treeview, this route is accessed and test cases are displayed   
@app.route('/module/<int:module_id>')
def get_module_details(module_id):
    module = Module.query.get_or_404(module_id)
    test_cases = TestCase.query.filter_by(module_id=module_id).all()
    return jsonify({
        'module': {
            'id': module.id,
            'name': module.name
        },
        'test_cases': [{
            'id': tc.id,
            'title': tc.title,
            'description': tc.description,
            
        } for tc in test_cases]
    })
##This module below is used to ADD a Module
@app.route('/module', methods=['POST'])
def add_module():
    data = request.json
    module = Module(
        name=data['name'],
        description=data.get('description', ''),
        parent_id=data.get('parent_id')
    )
    db.session.add(module)
    db.session.commit()
    
    child_count = Module.query.filter_by(parent_id=module.id).count()
    return jsonify({
        'id': module.id,
        'name': module.name,
        'text': f"{module.name} ({child_count})" if child_count > 0 else module.name
    })


#-----------Test related routes---------------------
##Used to add a testcase
@app.route('/testcase', methods=['POST'])
def add_test_case():
    data = request.json
    test_case = TestCase(
        title=data['title'],
        description=data.get('description', ''),
        module_id=data['module_id']
    )
    db.session.add(test_case)
    db.session.commit()


    module = Module.query.filter_by(id=data['module_id']).first()
    send_slack_notification(f"New Test Case Added: <{test_case.title}> in <{module.name}>")
    
    return jsonify({'id': test_case.id, 'title': test_case.title})

##Used to get,edit,delete a testcase
### Get => To populate popup fields     - Activated when "edit" icon is clicked
### Put => To edit test case            - Activated when "Save" button on pop up is clicked 
### Get => To populate popup fields     - Activated when "delete" button is clicked
@app.route('/testcase/<int:testcase_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_test_case(testcase_id):
    test_case = TestCase.query.get_or_404(testcase_id)
    
    print(request.method,test_case)
    if request.method == 'GET':
        return jsonify({
            'id': test_case.id,
            'title': test_case.title,
            'description': test_case.description,
            'filename': test_case.filename,
        })

    elif request.method == 'PUT':
        data = request.json
        old = test_case.title
        test_case.title = data['title']
        test_case.description = data['description']

        db.session.commit()
        
        module = Module.query.filter_by(id=test_case.module_id).first()
        
        send_slack_notification(f"Old Test Case <{old}> edited to <{test_case.title}> in <{module.name}>")
        
        return jsonify({
            'id': test_case.id,
            'title': test_case.title,
            'description': test_case.description,
        })

    elif request.method == 'DELETE':
        db.session.delete(test_case)
        db.session.commit()

        module = Module.query.filter_by(id=test_case.module_id).first()
   
        send_slack_notification(f"Test Case Deleted: <{test_case.title}> in <{module.name}>")
        
        return jsonify({'message': 'Test case is deleted'}), 204
    

#----Module Delete----#
@app.route('/module/<int:module_id>', methods=['DELETE'])
def delete_module(module_id):
    module = Module.query.get(module_id)
    if not module:
        return jsonify({"error": "Module not found"}), 404

    db.session.delete(module)
    db.session.commit()
    return jsonify({"message": "Module deleted successfully"}), 200


#----File upload----#
@app.route('/testcase/<int:testcase_id>/upload', methods=['POST'])
def upload_file(testcase_id):
    test_case = TestCase.query.get_or_404(testcase_id)

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    test_case.filename = file.filename
    test_case.data = file.read()

    db.session.commit()
    return jsonify({"message": "File uploaded successfully"}), 200


#----File download----#
@app.route('/download/<int:testcase_id>', methods=['GET'])
def download_file(testcase_id):
    test_case = TestCase.query.get_or_404(testcase_id)
    if not test_case.data:
        return jsonify({"error": "No file attached"}), 404

    return Response(
        test_case.data,
        mimetype="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment;filename={test_case.filename}"
        }
    )

if __name__ == '__main__':
    create_db(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
