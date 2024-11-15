from models import db  # Import the Flask app to access its context
from models import Module,TestCase  # Import your models to ensure they're loaded
from sqlalchemy import inspect
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
load_dotenv()


def create_db(app):
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT") 

    conn = psycopg2.connect(
        dbname='postgres',  
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
    exists = cursor.fetchone()

    if not exists:
        print(f"Database '{db_name}' does not exist. Creating...")
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        print(f"Database '{db_name}' created.")
    else:
        print(f"Database '{db_name}' already exists.")

    
    cursor.close()
    conn.close()
    
    with app.app_context():  
        
        inspector = inspect(db.engine)
        
        # Check if 'modules' table exists
        if not inspector.has_table('modules'):
            print("modules table does not exist, creating...")
            db.create_all()  # Create the table if it does not exist
        else:
            print("modules table already exists.")
        
        # Check if 'test_cases' table exists
        if not inspector.has_table('test_cases'):
            print("test_cases table does not exist, creating...")
            db.create_all()  
        else:
            print("test_cases table already exists.")
        
        
        if Module.query.count() == 0:
            print("Adding default teams...")
            module1 = Module(name='Blog')
            module2 = Module(name='Footer section')
            module3 = Module(name='Pricing')
            module4 = Module(name='Header section')
            db.session.add_all([module1, module2, module3,module4])
            db.session.commit()
        
        
            module_ids = [module.id for module in Module.query.limit(3).all()]
            test1 = TestCase(title='test 1', description = "hello", module_id=module_ids[0])
            test2 = TestCase(title='test 2', description = "hello", module_id=module_ids[0])
            test3 = TestCase(title='test 3', description = "hello", module_id=module_ids[1])
            test4 = TestCase(title='test 4', description = "hello", module_id=module_ids[1])
            test5 = TestCase(title='test 5', description = "hello", module_id=module_ids[2])
            test6 = TestCase(title='test 6', description = "hello", module_id=module_ids[2])
            db.session.add_all([test1, test2, test3, test4, test5, test6])
            db.session.commit()

        print("Database structure is ready with default data!")

if __name__ == '__main__':
    create_db()