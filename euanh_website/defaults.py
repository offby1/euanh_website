import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from euanh_website.models import CommonBase

engine = create_engine(os.environ["DATABASE_URL"])
CommonBase.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


default_jinja_config = {
    "site_name": "Euan's Blog",
}
