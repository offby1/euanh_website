from datetime import datetime

from sqladmin import ModelView
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from euanh_website.models.Base import CommonBase


class BlogPost(CommonBase):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    preview = Column(String)
    content = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="blog_posts")

    def __repr__(self):
        return f"<BlogPost {self.title}>"

    def __str__(self):
        return self.title


class BlogPostView(ModelView, model=BlogPost):
    column_list = [
        BlogPost.id,
        BlogPost.title,
        BlogPost.preview,
        BlogPost.author,
        BlogPost.created_on,
        BlogPost.updated_on,
    ]

    form_excluded_columns = ["created_on", "updated_on"]

    column_default_sort = ("created_on", True)
