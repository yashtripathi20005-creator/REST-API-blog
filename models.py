# models.py
from datetime import datetime

class Post:
    """Blog post model."""
    def __init__(self, post_id, title, content, author="Anonymous", created_at=None):
        self.post_id = post_id
        self.title = title
        self.content = content
        self.author = author
        self.created_at = created_at or datetime.utcnow().isoformat()

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'post_id': self.post_id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Post from a dictionary."""
        return cls(
            post_id=data['post_id'],
            title=data['title'],
            content=data['content'],
            author=data.get('author', 'Anonymous'),
            created_at=data.get('created_at')
        )

class Comment:
    """Comment model for blog posts."""
    def __init__(self, comment_id, post_id, content, author="Anonymous", created_at=None):
        self.comment_id = comment_id
        self.post_id = post_id
        self.content = content
        self.author = author
        self.created_at = created_at or datetime.utcnow().isoformat()

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'comment_id': self.comment_id,
            'post_id': self.post_id,
            'content': self.content,
            'author': self.author,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Comment from a dictionary."""
        return cls(
            comment_id=data['comment_id'],
            post_id=data['post_id'],
            content=data['content'],
            author=data.get('author', 'Anonymous'),
            created_at=data.get('created_at')
        )
