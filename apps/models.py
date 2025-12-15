from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Message(Base):
    __tablename__= "messages"

    id = Column(Integer, primary_key=True, nullable=False)
    sender_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    content = Column(String, nullable=False)
    seen = Column(Boolean, server_default='TRUE', nullable=False)
    time_stamp = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    
    parent_message_id = Column(Integer, ForeignKey(
    "messages.id", ondelete="CASCADE"), nullable=True)
    
    # sender = relationship("User")
    # receiver = relationship("User")

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
    replyOf = relationship("Message", foreign_keys=[parent_message_id])



class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    