import os
from app import create_app,db
from app.models import User,Role
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand
app = create_app('default')
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)



@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
