from sqladmin import ModelView

from euanh_website.models import BlogPost


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
