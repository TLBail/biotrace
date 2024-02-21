from sqlalchemy import Integer, String, Enum, DateTime, text, BLOB
from sqlalchemy.orm import mapped_column, Mapped

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class File(db.Model):
    __tablename__ = 'file'

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type : Mapped[str] = mapped_column(Enum('log', 'config'), nullable=False)
    name : Mapped[str] = mapped_column(String(255), nullable=False)
    content : Mapped[str] = mapped_column(BLOB, nullable=False)  # Assuming BLOB as String for simplicity
    created_at : Mapped[str] = mapped_column(DateTime, server_default=text('NOW()'), nullable=False)
    updated_at : Mapped[str] = mapped_column(DateTime, server_default=text('NOW()'), nullable=False)
    deleted_at : Mapped[str] = mapped_column(DateTime, comment='paranoid table', default=None)