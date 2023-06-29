from app import db, create_app
from config import config
from constants import PORT
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(config.get(PORT, 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
