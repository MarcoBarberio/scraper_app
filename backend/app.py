from flask import Flask
import backend.routes as routes
def create_app():
    app=Flask(__name__)
    app.register_blueprint(routes.blueprint)
    return app