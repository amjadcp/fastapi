import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="2233", cursor_factory=RealDictCursor)
cur = conn.cursor()


app = FastAPI()

messages = []

class Post(BaseModel):
    id : int
    message : str

class Put(BaseModel):
    message : str

@app.post('/message_post', status_code=status.HTTP_201_CREATED)
async def message_post(post:Post):
    cur.execute("""insert into messages (id, message) values (%s, %s)""", (post.id, post.message))
    conn.commit()
    return status.HTTP_201_CREATED

@app.get('/message_get', status_code=status.HTTP_200_OK)
async def message_get():
    cur.execute("SELECT * FROM messages;")
    data = cur.fetchall()
    return data

@app.get('/message_find/{id}', status_code=status.HTTP_302_FOUND)
async def message_find(id:int):
    try:
        cur.execute("select * from messages where id=%s", str(id))
        data = cur.fetchone()
        return data
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.put('/message_update/{id}', status_code=status.HTTP_200_OK)
async def message_update(id:int, put:Put):
    try:
        cur.execute("update messages set message=%s where id=%s", (put.message, str(id)))
        # conn.commit()
        return status.HTTP_200_OK
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.delete('/message_delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def message_delete(id:int):
    try:
        cur.execute("delete from messages where id=%s", str(id))
        return status.HTTP_204_NO_CONTENT
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


