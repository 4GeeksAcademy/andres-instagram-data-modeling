import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    profile_name = Column(String(50), nullable=False)
    followers = relationship("Followers", foreign_keys="[Followers.followed_id]")
    followed = relationship("Followers", foreign_keys="[Followers.follower_id]")

class Followers(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('user.id'))
    followed_id = Column(Integer, ForeignKey('user.id'))

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    created_by_user_id = Column(Integer, ForeignKey('user.id'))
    location = Column(String(250), nullable=False)
    caption = Column(String(250), nullable=True)
    user = relationship("User")
    likes = relationship("Likes")
    comments = relationship("Comment")
    media_type = relationship("MediaType")

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    posted_by_user = Column(Integer, ForeignKey('user.id'))
    comment_on_post = Column(String(350), nullable=False)

class Likes(Base):
    __tablename__ = 'likes'
    id_user = Column(Integer, ForeignKey('user.id'), primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), primary_key=True)

class MediaType(Base):
    __tablename__ = 'media_type'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    media_file = Column(String(250), nullable=False)
    post = relationship("Post")

    def to_dict(self):
        return {}


## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
