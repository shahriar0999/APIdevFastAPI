


@app.get("/posts", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts =  cursor.fetchall()
    posts = db.query(models.Post).all()
    return {'message': posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def createPost(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)  RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # this line is of code inefficient cause when we have so many columns then it takes lots of time
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    # easy way to do that
    new_post = models.Post(
        **post.dict())
    # add that new post into database
    db.add(new_post)
    # push this post into database
    db.commit()
    # and display that crated post
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (id,))
    # conn.commit()
    # deleted_post = cursor.fetchone()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() == None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
