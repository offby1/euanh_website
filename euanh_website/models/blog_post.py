from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from euanh_website.models.base import CommonBase


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
