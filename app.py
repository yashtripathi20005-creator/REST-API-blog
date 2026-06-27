# app.py
from flask import Flask, request, jsonify
from storage import Storage
from models import Post, Comment
import uuid

app = Flask(__name__)
storage = Storage()

# Helper to generate unique IDs
def generate_id():
    return str(uuid.uuid4())

# ---------- POSTS ----------
@app.route('/posts', methods=['GET'])
def get_posts():
    """Return all blog posts."""
    posts = storage.get_all_posts()
    return jsonify([post.to_dict() for post in posts]), 200

@app.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    """Return a single post by ID."""
    post = storage.get_post(post_id)
    if post:
        return jsonify(post.to_dict()), 200
    return jsonify({"error": "Post not found"}), 404

@app.route('/posts', methods=['POST'])
def create_post():
    """Create a new blog post."""
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Title and content are required"}), 400
    
    post = Post(
        post_id=generate_id(),
        title=data['title'],
        content=data['content'],
        author=data.get('author', 'Anonymous')
    )
    storage.add_post(post)
    return jsonify(post.to_dict()), 201

@app.route('/posts/<post_id>', methods=['PUT'])
def update_post(post_id):
    """Update an existing post."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400
    
    post = storage.get_post(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    
    # Update fields if provided
    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']
    if 'author' in data:
        post.author = data['author']
    
    storage.update_post(post)
    return jsonify(post.to_dict()), 200

@app.route('/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post and its comments."""
    if storage.delete_post(post_id):
        return jsonify({"message": "Post deleted"}), 200
    return jsonify({"error": "Post not found"}), 404

# ---------- COMMENTS ----------
@app.route('/posts/<post_id>/comments', methods=['GET'])
def get_comments(post_id):
    """Get all comments for a post."""
    if not storage.get_post(post_id):
        return jsonify({"error": "Post not found"}), 404
    comments = storage.get_comments_for_post(post_id)
    return jsonify([c.to_dict() for c in comments]), 200

@app.route('/posts/<post_id>/comments', methods=['POST'])
def add_comment(post_id):
    """Add a comment to a post."""
    if not storage.get_post(post_id):
        return jsonify({"error": "Post not found"}), 404
    
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({"error": "Comment content is required"}), 400
    
    comment = Comment(
        comment_id=generate_id(),
        post_id=post_id,
        content=data['content'],
        author=data.get('author', 'Anonymous')
    )
    storage.add_comment(comment)
    return jsonify(comment.to_dict()), 201

@app.route('/comments/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """Delete a comment by ID."""
    if storage.delete_comment(comment_id):
        return jsonify({"message": "Comment deleted"}), 200
    return jsonify({"error": "Comment not found"}), 404

# ---------- HEALTH CHECK ----------
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
