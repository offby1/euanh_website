from sqlalchemy import create_engine

from euanh_website.models import CommonBase

engine = create_engine("sqlite:///euanh_website.db")
CommonBase.metadata.create_all(engine)
