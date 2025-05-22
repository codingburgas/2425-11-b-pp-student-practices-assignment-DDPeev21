from app import create_app
from app.extensions import db
from flask_migrate import upgrade

app = create_app()

# Optional: Automatically upgrade database on first run (not needed in dev usually)
@app.before_first_request
def initialize_database():
    upgrade()

if __name__ == '__main__':
    app.run(debug=True)

