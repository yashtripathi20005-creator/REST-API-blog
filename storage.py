# storage.py
import json
import os
from models import Post, Comment

class Storage:
    """
    Simple file-based storage for posts and comments.
    Data is persisted in posts.json and comments.json.
    """
    def __init__(self, posts_file='posts.json', comments_file='comments.json'):
        self.posts_file = posts_file
        self.comments_file = comments_file
        self.posts = []
        self.comments = []
        self._load_data()

    def _load_data(self):
        """Load posts and comments from JSON files."""
        # Load posts
        if os.path.exists(self.posts_file):
            with open(self.posts_file, 'r') as f:
                posts_data = json.load(f)
                self.posts = [Post.from_dict(p) for p in posts_data]
        else:
            self.posts = []

        # Load comments
        if os.path.exists(self.comments_file):
            with open(self.comments_file, 'r') as f:
                comments_data = json.load(f)
                self.comments = [Comment.from_dict(c) for c in comments_data]
        else:
            self.comments = []

    def _save_data(self):
        """Save posts and comments to JSON files."""
        with open(self.posts_file, 'w') as f:
            json.dump([p.to_dict() for p in self.posts], f, indent=2)
        with open(self.comments_file, 'w') as f:
            json.dump([c.to_dict() for c in self.comments], f, indent=2)

    # ---- Posts ----
    def get_all_posts(self):
        """Return all posts sorted by creation date (newest first)."""
        return sorted(self.posts, key=lambda p: p.created_at, reverse=True)

    def get_post(self, post_id):
        """Return a single post by ID or None."""
        for post in self.posts:
            if post.post_id == post_id:
                return post
        return None

    def add_post(self, post):
        """Add a new post."""
        self.posts.append(post)
        self._save_data()

    def update_post(self, updated_post):
        """Update an existing post."""
        for i, post in enumerate(self.posts):
            if post.post_id == updated_post.post_id:
                self.posts[i] = updated_post
                self._save_data()
                return True
        return False

    def delete_post(self, post_id):
        """Delete a post and its associated comments."""
        # Delete post
        post_deleted = False
        for i, post in enumerate(self.posts):
            if post.post_id == post_id:
                self.posts.pop(i)
                post_deleted = True
                break
        
        if not post_deleted:
            return False
        
        # Delete associated comments
        self.comments = [c for c in self.comments if c.post_id != post_id]
        self._save_data()
        return True

    # ---- Comments ----
    def get_comments_for_post(self, post_id):
        """Return all comments for a specific post."""
        return [c for c in self.comments if c.post_id == post_id]

    def add_comment(self, comment):
        """Add a new comment."""
        self.comments.append(comment)
        self._save_data()

    def delete_comment(self, comment_id):
        """Delete a comment by ID."""
        for i, comment in enumerate(self.comments):
            if comment.comment_id == comment_id:
                self.comments.pop(i)
                self._save_data()
                return True
        return False
