import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from euanh_website.models import CommonBase

engine = create_engine(os.environ["DATABASE_URL"])
CommonBase.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


default_jinja_config = {
    "site_name": "Euan's Blog",
    "current_year": datetime.now().year,
}

site_mapping = {
    "blog_posts": "/blog_posts",
    "view_blog_post": "/blog_posts/{id}",
    "about": "/about",
    "contact": "/contact",
    "home": "/",
    "admin": "/the_most_secret_admin_page_in_the_world",
}
