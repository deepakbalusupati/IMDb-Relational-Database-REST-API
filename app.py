from flask import Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from database.db_connection import init_db
from routes.api_routes import initialize_routes
from routes.web_routes import web_bp
from config.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# Initialize database
init_db(app)

# Register blueprints
app.register_blueprint(web_bp)

# REST API
api = Api(app)
initialize_routes(api)

# Swagger UI
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "IMDb API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)