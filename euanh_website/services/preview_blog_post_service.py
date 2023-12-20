import mistune

from euanh_website import defaults
from euanh_website.defaults import Session
from euanh_website.models import BlogPost


class PreviewBlogPostService:
    @classmethod
    def get_post_url(cls, post_id):
        return defaults.site_mapping["view_blog_post"].format(id=post_id)

    @classmethod
    def format_posts(cls, posts):
        for post in posts:
            post["url"] = cls.get_post_url(post["id"])
            post["preview"] = mistune.html(post["preview"])
            post["updated_on"] = post["updated_on"].strftime("%d %B %Y")

        return posts

    @classmethod
    def get_all(cls):
        with Session() as session:
            posts = (
                session.query(BlogPost)
                .order_by(BlogPost.updated_on.desc())
                .filter(BlogPost.is_published == True)
                .all()
            )

            return cls.format_posts([post.__dict__ for post in posts])

    @classmethod
    def get_latest(cls, limit=6):
        with Session() as session:
            posts = (
                session.query(BlogPost)
                .order_by(BlogPost.updated_on.desc())
                .filter(BlogPost.is_published == True)
                .limit(limit)
                .all()
            )

            return cls.format_posts([post.__dict__ for post in posts])

    @classmethod
    def get(cls, id):
        with Session() as session:
            post = (
                session.query(BlogPost)
                .filter(BlogPost.is_published == True)
                .filter(BlogPost.id == id)
                .first()
            )

            if post is None:
                return None
            return post.__dict__
