




@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash the password -> user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    # easy way to do that
    new_user = models.User(
        **user.dict())
    # add that new post into database
    db.add(new_user)
    # push this post into database
    db.commit()
    # and display that crated post
    db.refresh(new_user)
    return new_user

@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    return user