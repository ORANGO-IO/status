from web import create_app
from web.services.scheduler import start_scheduler

app = create_app()

with app.app_context():
    start_scheduler(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)