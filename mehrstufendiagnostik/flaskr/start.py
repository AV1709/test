from flask import Flask
import datetime

def startUp():
    print("Starting backend initialization...")


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    import mehrstufendiagnostik.flaskr.blog

    app.register_blueprint(mehrstufendiagnostik.flaskr.blog.bp)
    app.add_url_rule('/', endpoint='index')

    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)

    return app

if __name__ == "__main__":
    startUp()
    app = create_app()
    app.run(host="localhost", port=8080)