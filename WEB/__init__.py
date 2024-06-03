from flask import Flask, render_template, url_for
from .views import main_views

def create_app():
    app = Flask(__name__)
    app.secret_key = '00'

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/info/')
    def info():
        return render_template('info.html')

    app.register_blueprint(main_views.databp)    

    return app