from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True) 
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    posts: Mapped[list["Post"]] = relationship(back_populates="author")
    comment: Mapped[list["Comment"]] = relationship(back_populates="user")
    likes: Mapped[list["Like"]] = relationship(back_populates="user")
    following: Mapped[list["Follow"]] = relationship(foreign_keys=["Follow.follower_id"], back_populates="follower") # Подписка пользователя на других
    followers: Mapped[list["Follow"]] = relationship(foreign_keys=["Follow.followed_id"], back_populates="followed") #  Подписки других на пользователя
    
    
class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    tittle: Mapped[str] = mapped_column(String(30), nullable=True)
    context: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    author: Mapped["User"] = relationship(back_populates="posts") 
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")
    likes: Mapped[list["Like"]] = relationship(back_populates="post")
    follows: Mapped[list["Follow"]] = relationship(back_populates="follower")


class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(300), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    
    user: Mapped["User"] = relationship(back_populates="comment")
    post: Mapped["Post"] = relationship(back_populates="comments")
    

class Like(Base):
    __tablename__ = "likes"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id")) 
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    
    user: Mapped["User"] = relationship(back_populates="likes")
    post: Mapped["Post"] = relationship(back_populates="likes")
    
    
class Follow(Base):
    __tablename__ = "follows"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id")) # ID Пользователя который подписывается
    followed_id: Mapped[int] = mapped_column(ForeignKey("users.id")) # ID Пользоваетля на которого подписываются
    
    follower: Mapped["User"] = relationship(foreign_keys=[follower_id], back_populates="following")
    followed: Mapped["User"] = relationship(foreign_keys=[followed_id], back_populates="followers")