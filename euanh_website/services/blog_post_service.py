import mistune

from euanh_website.defaults import Session
from euanh_website.models import BlogPost


class BlogPostService:
    @classmethod
    def format_post(cls, post):
        post["content"] = mistune.html(post["content"])
        post["updated_on"] = post["updated_on"].strftime("%d %B %Y")

        print(post["content"])
        return post

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
            return cls.format_post(post.__dict__)
