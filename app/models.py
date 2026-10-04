from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column 
from sqlalchemy import Integer, String
import asyncio

class Base(DeclarativeBase):
    pass

class Note(Base):
    __tablename__ = "Notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(200), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)






