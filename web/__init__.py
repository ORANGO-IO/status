from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from web.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(
        __name__,
        template_folder=Config.TEMPLATE_FOLDER,
        static_folder=Config.STATIC_FOLDER
    )
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    print("Importando os modelos...")
    import web.models  # Importa os modelos para que o Flask-Migrate possa encontrá-los

    # Importa e registra as rotas
    from web.routes import main_routes
    app.register_blueprint(main_routes)

    from web.services.scheduler import start_scheduler
    start_scheduler()

    return app