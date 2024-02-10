'''
Create an actual database later for scalability
'''

from app import db, create_app

def init_db():
    app = create_app()
    with app.app_context():
        # Drop all tables to start fresh; comment this out if you don't want to lose data
        # db.drop_all()
        # Create all tables
        db.create_all()
        print("Initialized the database.")

if __name__ == '__main__':
    init_db()

