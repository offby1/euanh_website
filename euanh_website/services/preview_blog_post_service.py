from euanh_website import defaults
from euanh_website.defaults import Session
from euanh_website.models import BlogPost


class PreviewBlogPostService:
    @classmethod
    def get_post_url(cls, post_id):
        return defaults.site_mapping["view_blog_post"].format(id=post_id)

    @classmethod
    def set_urls_for_posts(cls, posts):
        for post in posts:
            post["url"] = cls.get_post_url(post["id"])

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

            return cls.set_urls_for_posts([post.__dict__ for post in posts])

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

            return cls.set_urls_for_posts([post.__dict__ for post in posts])

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
