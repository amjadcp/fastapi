from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import null

# import psycopg2
# from psycopg2.extras import RealDictCursor

# conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="2233", cursor_factory=RealDictCursor)
# cur = conn.cursor()

import models
from database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

messages = []

class Post(BaseModel):
    id : int
    message : str

class Put(BaseModel):
    message : str

@app.post('/message_post', status_code=status.HTTP_201_CREATED)
async def message_post(post:Post, db:Session=Depends(get_db)):
    # cur.execute("""insert into messages (id, message) values (%s, %s)""", (post.id, post.message))
    # conn.commit()
    data = models.Messages(id=post.id, message=post.message)
    db.add(data)
    db.commit()
    return status.HTTP_201_CREATED

@app.get('/message_get', status_code=status.HTTP_200_OK)
async def message_get(db: Session=Depends(get_db)):
    # cur.execute("SELECT * FROM messages;")
    # data = cur.fetchall()
    data = db.query(models.Messages).all()
    return data

@app.get('/message_find/{id}', status_code=status.HTTP_302_FOUND)
async def message_find(id:int, db:Session=Depends(get_db)):
    try:
        # cur.execute("select * from messages where id=%s", str(id))
        # data = cur.fetchone()

        data = db.query(models.Messages).filter(models.Messages.id == id).first()

        if not data:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        else:
            return data
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.put('/message_update/{id}', status_code=status.HTTP_200_OK)
async def message_update(id:int, put:Put, db:Session=Depends(get_db)):
    try:
        # cur.execute("update messages set message=%s where id=%s", (put.message, str(id)))

        data_query = db.query(models.Messages).filter(models.Messages.id == id)
        if not data_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        else:
            data_query.update({'message':put.message}, synchronize_session=False)
            db.commit()
            return status.HTTP_200_OK
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.delete('/message_delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def message_delete(id:int, db:Session=Depends(get_db)):
    try:
        # cur.execute("delete from messages where id=%s", str(id))
        data_query = db.query(models.Messages).filter(models.Messages.id == id)

        if not data_query.first():
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        else:
            data_query.delete(synchronize_session=False)
            db.commit()
            return status.HTTP_204_NO_CONTENT

    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


