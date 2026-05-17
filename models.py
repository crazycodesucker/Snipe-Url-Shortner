from sqlalchemy import Column, Integer, String
from database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    slug = Column(
        String,
        unique=True,
        nullable=False
    )

    url = Column(
        String,
        nullable=False
    )

    clicks = Column(
        Integer,
        default=0
    )