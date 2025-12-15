from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, outh2



router = APIRouter(
    prefix="/users",
    tags=['Posts']
)


@router.get("/", response_model=list[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.created_at).all()
    return users


@router.get("/{id}", response_model=schemas.UserOut)
def get_user_by_id(id:int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id==id).first()
    return user 


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_a_user(user: schemas.UserIn, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return "user have created successfully"

@router.put("/password-change", status_code=status.HTTP_201_CREATED)
def change_user_password(user: schemas.UserPasswordChange, db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user)):

    user_query = db.query(models.User).filter(models.User.id == current_user.id)

    this_user=user_query.first()

    print(this_user.email)
    print(this_user.password)

    print(user.password)
    print(user.new_password)


    


    if this_user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only can perform own password change")

     
    


    print(user.email)
    print(user.password)

    if (this_user.email == user.email and utils.verify(user.password, this_user.password)):
        
        new_password = utils.hash(user.new_password)

        user_query.update({"password": new_password}, synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="email or password did not matched")

    return "password have Updated successfully"



