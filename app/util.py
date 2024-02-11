from flask import current_app
from contextlib import contextmanager

@contextmanager
def get_app_context():
    # Get app context
    app = current_app._get_current_object()
    with app.app_context():
        yield