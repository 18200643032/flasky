import os
import click
from app import create_app,db
from app.models import User,Role
from flask_migrate import Migrate
app = create_app('default')
#app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
migrate = Migrate(app,db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,User=User,Role=Role)


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_name):
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
