from database import Base
from sqlalchemy import String, Integer, Column, Float
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, ForeignKey=("likes.user_id"), index=True, unique=True)
    username = Column(String)
    mail = Column(String)
    password = Column(String)
    image_path = Column(String)

    pet_projects = relationship("PetProjects", back_populates="users")
    likes = relationship("Likes", back_populates="users")

class Likes(Base):
    __tablename__ = "likes"
    like_id = Column(Integer)
    user_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)

    users = relationship("Users", back_populates="likes")
    pet_projects = relationship("PetProjects", back_populates="likes")

class PetProjects(Base):
    __tablename__ = "pet_projects"
    project_id = Column(Integer, ForeignKey=("likes.project_id"), unique=True)
    user_id = Column(Integer, ForeignKey=("users.user_id"), unique=True)
    theme_id = Column(Integer, ForeignKey("themes.theme_id"), unique=True)
    title = Column(String)
    short_description = Column(String)
    description = Column(String)
    average_score = Column(Float(precision=53))

    users = relationship("Users", back_populates="pet_projects")
    likes = relationship("Likes", back_populates="pet_projects")
    themes = relationship("themes", back_populates="pet_projects")

class Themes(Base):
    __tablename__ = "themes"
    theme_id = Column(Integer, primary_key=True, index=True)
    theme_name = Column(String)

    pet_projects = relationship("PetProjects", back_populates="themes")