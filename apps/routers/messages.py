from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, outh2


from typing import List, Optional


router = APIRouter(
    prefix="/messages",
    tags=['Messages']
)


@router.get("/read", response_model = list[schemas.MessageOut])
def get_messages(db: Session = Depends(get_db)):
    # messages = db.query(models.Message).group_by(models.Message.sender_id).order_by(models.Message.time_stamp).all()
    messages = db.query(models.Message).order_by(models.Message.time_stamp).all()

    return messages
              
@router.get("/{id}", response_model = list[schemas.MessageOut])
def get_message_by_sender_id(id:int, db: Session = Depends(get_db)):

    messages = db.query(models.Message).filter(models.Message.sender_id == id).order_by(models.Message.time_stamp).all()

    return messages

@router.post("/{rec_id}")
def send_message(rec_id: int, message: schemas.MessageIn, db: Session = Depends(get_db), current_user= Depends(outh2.get_current_user)):
    
    new_message = models.Message(sender_id=current_user.id, receiver_id=rec_id, **message.model_dump())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return "Done, message have been sent"

@router.post("/{rec_id}/{par_id}")
def reply_to_a_message(rec_id: int, par_id: int, message: schemas.MessageIn, db: Session = Depends(get_db), current_user= Depends(outh2.get_current_user)):
    
    new_message = models.Message(sender_id=current_user.id, receiver_id=rec_id, parent_message_id=par_id, **message.model_dump())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return "Done, reply have been sent"


# @router.post("/{rec_id}")
# @router.post("/{rec_id}/{par_id}")

# can i make these two one, by applying a optional in the path parameter, and then in the query.
# like, # @router.post("/{rec_id}/optional{par_id}"), if par_id available the it is a reply, otherwise a message. (run queries in the condition)
# also can i provide those automatically in the frontend, coz, when giving a message or replying to a message the app should somehow take in the reciever id and then the parent message id.

@router.put("/update/{mes_id}", response_model = schemas.MessageOut)
def update_a_message(mes_id: int, Updated_message: schemas.MessageIn, db: Session = Depends(get_db)):
    
    message_query = db.query(models.Message).filter(models.Message.id == mes_id)

    message_query.update(Updated_message.model_dump(), synchronize_session=False)

    db.commit()

    final_message = message_query.first()

    return final_message


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(id: int, db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user)):

    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    message_query = db.query(models.Message).filter(models.Message.id == id)

    message = message_query.first()

    if message == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if message.sender_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    message_query.delete(synchronize_session=False)
    db.commit()

    return Response (status_code=status.HTTP_204_NO_CONTENT)

