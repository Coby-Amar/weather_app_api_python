def create_app():
    import datetime
    import dotenv
    from os import environ
    from flask import Flask
    from flask_cors import CORS
    from api import auth, users
    from api.modules import db, bcrypt, jwt

    app = Flask(__name__)
    dotenv.load_dotenv()

    app.config["JWT_CSRF_IN_COOKIES"] = True
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=7)

    app.config['SECRET_KEY'] = environ.get("SECRET")
    app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET_KEY")
    app.config["JWT_COOKIE_SAMESITE"] = environ.get("JWT_COOKIE_SAMESITE")
    app.config["JWT_COOKIE_SECURE"] = environ.get("JWT_COOKIE_SECURE")
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get(
        "SQLALCHEMY_DATABASE_URI")

    isDev = environ.get("MODE") == 'DEV'
    if isDev:
        CORS(app, supports_credentials=True)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(auth.auth_api, url_prefix='/auth')
    app.register_blueprint(users.users_api, url_prefix='/user')
    return app


app = create_app()


@app.get('/')
def index():
    return 'Whoops'


if __name__ == '__main__':
    app.run(debug=True)
