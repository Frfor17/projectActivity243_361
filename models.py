from database import Base
from sqlalchemy import String, Integer, Column, Float, ForeignKey
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True, unique=True)
    username = Column(String)
    mail = Column(String)
    password = Column(String)
    image_path = Column(String)

    # pet_projects = relationship("PetProjects", back_populates="users")
    likes = relationship("Likes", back_populates="users")


class Likes(Base):
    __tablename__ = "likes"
    like_id = Column(Integer, primary_key=True)  # Добавлен primary_key
    user_id = Column(Integer, ForeignKey("users.user_id"))
    project_id = Column(Integer, ForeignKey("pet_projects.project_id"), primary_key=True, index=True)  # Исправлен внешний ключ
    score = Column(Integer)

    users = relationship("Users", back_populates="likes")
    # pet_projects = relationship("PetProjects", back_populates="likes")



class PetProjects(Base):
    __tablename__ = "pet_projects"
    project_id = Column(Integer, primary_key=True)  # Исправлено на primary_key
    user_id = Column(Integer, ForeignKey("users.user_id"))
    theme_id = Column(Integer, ForeignKey("themes.theme_id"))
    title = Column(String)
    short_description = Column(String)
    description = Column(String)
    average_score = Column(Float(precision=53))

#     users = relationship("Users", back_populates="pet_projects")
#     likes = relationship("Likes", back_populates="pet_projects")
#     themes = relationship("Themes", back_populates="pet_projects")


# class Themes(Base):
#     __tablename__ = "themes"
#     theme_id = Column(Integer, primary_key=True, index=True)
#     theme_name = Column(String)

#     pet_projects = relationship("PetProjects", back_populates="themes")
