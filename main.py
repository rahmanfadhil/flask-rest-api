from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)

class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content')

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

class PostsResource(Resource):
    def get(self):
        return posts_schema.dump(Post.query.all())
    
    def post(self):
        data = request.json
        post = Post(title=data['title'], content=data['content'])
        db.session.add(post)
        db.session.commit()
        return post_schema.dump(post)

class PostResource(Resource):
    def get(self, pk):
        return post_schema.dump(Post.query.get_or_404(pk))

    def patch(self, pk):
        data = request.json
        post = Post.query.get_or_404(pk)

        if 'title' in data:
            post.title = data['title']
        
        if 'content' in data:
            post.content = data['content']
        
        db.session.commit()
        return post_schema.dump(post)

    def delete(self, pk):
        post = Post.query.get_or_404(pk)
        db.session.delete(post)
        db.session.commit()
        return '', 204

api.add_resource(PostResource, '/post/<int:pk>')
api.add_resource(PostsResource, '/posts')

if __name__ == '__main__':
    app.run(debug=True)
