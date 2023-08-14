from app import create_app, db
from app.models.main import User, Role
from flask_migrate import Migrate


app = create_app()
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('unittests')
    unittest.TextTestRunner(verbosity=2).run(tests)
