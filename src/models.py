from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    __tablename__ = "character"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    age: Mapped[str] = mapped_column(String(5), nullable=False)
    height: Mapped[str] = mapped_column(String(5), nullable=True)
    weight: Mapped[str] = mapped_column(String(5), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "height": self.height,
            "weight": self.weight
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    age: Mapped[str] = mapped_column(String(5), nullable=False)
    color: Mapped[str] = mapped_column(String(20), nullable=False)
    population: Mapped[str] = mapped_column(nullable=True)
    density: Mapped[str] = mapped_column(nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "color": self.color,
            "population": self.population,
            "density": self.density
        }


class Favorite_character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    character_id: Mapped[int] = mapped_column(
        ForeignKey('character.id'), nullable=False)
    user: Mapped["User"] = db.relationship("User")
    character: Mapped["Character"] = db.relationship("Character")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user.id,              
            "character_id": self.character.id,
            
        }


class Favorite_Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), nullable=False)
    user: Mapped["User"] = db.relationship("User")
    planet: Mapped["Planet"] = db.relationship("Planet")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user.id,
            "planet_id": self.planet.id,
            
        }
