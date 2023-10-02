from fastapi import FastAPI,UploadFile,Response, HTTPException,Path
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

#SQLite 연결
con = sqlite3.connect('friend_db.db',check_same_thread=False)
cur=con.cursor()


cur.execute(f"""
            CREATE TABLE IF NOT EXISTS friends(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                phone_number TEXT NOT NULL
            )
           """)

app=FastAPI()

# 친구 추가
@app.post('/friends')
async def add_friend(name:str,phone_number:str):
    
    cur.execute(f"""
                INSERT INTO friends(name,phone_number)
                VALUES('{name}','{phone_number}')
                """)
    con.commit()
    
    return '200'

#친구 조회
@app.get('/friends')
async def list_friends():
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    rows=cur.execute(f"""
                     SELECT * FROM friends
                     """).fetchall()
    
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))
#친구 삭제
@app.delete('/friends/{friend_id}')
async def delete_friend(friend_id:int):
    cur.execute(f"""
                DELETE FROM friends
                WHERE id= {friend_id}
                """)
    con.commit()
    return '200'

#이름으로 친구 검색 
@app.get('/friends/{name}')
async def search_friend_by_name(name:str):
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    rows=cur.execute(f"""
                     SELECT * FROM friends
                     WHERE name="{name}"
                     """).fetchall()
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))
   

app.mount("/", StaticFiles(directory="frontend", html="True"), name="frontend")

