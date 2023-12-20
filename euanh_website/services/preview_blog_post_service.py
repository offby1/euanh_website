from euanh_website.defaults import Session
from euanh_website.models import BlogPost


class PreviewBlogPostService:
    @classmethod
    def get_all(cls):
        with Session() as session:
            posts = session.query(BlogPost).all()

            return [post.__dict__ for post in posts]

    @classmethod
    def get_latest(cls, limit=6):
        with Session() as session:
            posts = (
                session.query(BlogPost)
                .order_by(BlogPost.updated_on.desc())
                .limit(limit)
                .all()
            )

            return [post.__dict__ for post in posts]
