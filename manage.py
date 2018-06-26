import os
from app import create_app
from app.models import create_tables


create_app(os.getenv("APP_SETTINGS"))
create_tables()