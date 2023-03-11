
import configparser
import json
import urllib.parse
from typing import List, Union

import pandas as pd
import pyodbc
from api.auth import get_current_user
from config.config import pyodbc_connect, pyodbc_str
from database.crud import update_bienmuc, get_data_by_id
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.security import APIKeyCookie
from fastapi.templating import Jinja2Templates
from jose import JWTError
from models.bienmuc import Config
from pydantic import BaseModel

router = APIRouter()
cookie_sec = APIKeyCookie(name="session")
views = Jinja2Templates(directory='views')


def select(strSql):
    config = configparser.ConfigParser()
    config.read(r'config.ini')

    conn = pyodbc_connect('hn')

    cursor = conn.cursor()

    cursor.execute(strSql)

    records = cursor.fetchall()
    results = []
    columnNames = [column[0] for column in cursor.description]

    for record in records:
        results.append(dict(zip(columnNames, record)))

    json_results = json.dumps(results, ensure_ascii=False,
                              default=str)
    return json_results


@router.get("/view", response_class=HTMLResponse)
async def view(request: Request, tableName: str):
    df = pd.read_sql('select top(50) * from ' + tableName, pyodbc_str)
    # return Response(df.to_json(orient="records"), media_type="application/json")
    context = {'request': request, 'data': df.to_dict(orient='records'), 'columns': df.columns.values}
    return views.TemplateResponse('view.html', context)


@router.get("/sign-in", response_class=HTMLResponse)
async def details(request: Request):
    return views.TemplateResponse("base/sign-in.html", {"request": request})


@router.get("/home", response_class=HTMLResponse)
async def home(request: Request, username: str = Depends(get_current_user)):
    credentials_exception = HTTPException(
        status_code=401,
        # detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        return views.TemplateResponse("base/home.html", {"request": request})
    except JWTError:
        raise credentials_exception


@router.get("/data-entry", response_class=HTMLResponse)
async def data_entry(request: Request, username: str = Depends(get_current_user)):
    credentials_exception = HTTPException(
        status_code=401,
        # detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        data = json.loads(select('select duongdan from Config'))
        return views.TemplateResponse(
            "templates/data-entry.html",
            {"request": request, "data": data[0]})
    except JWTError:
        raise credentials_exception


@router.get("/convert", response_class=HTMLResponse)
async def convert(request: Request, username: str = Depends(get_current_user)):
    credentials_exception = HTTPException(
        status_code=401,
        # detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        return views.TemplateResponse("client/convert.html", {"request": request})
    except JWTError:
        raise credentials_exception


class FormRequest(BaseModel):
    dataForm: object


@router.post("/update-bienmuc")
async def update_biemuc(response: Response, request_data: FormRequest, request: Request, username: str = Depends(get_current_user)):
    credentials_exception = HTTPException(
        status_code=401,
        # detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        update_bienmuc('hn', Config, 85, request_data.dataForm)
        
        # print(request_data.dataForm)
        return 200
    except JWTError:
        raise credentials_exception
    

@router.get("/getdata")
async def update_biemuc(response: Response, request: Request, username: str = Depends(get_current_user)):
    credentials_exception = HTTPException(
        status_code=401,
        # detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        dataX = get_data_by_id('hn', Config, '85')
        
        return {"dataX": dataX}
    except JWTError:
        raise credentials_exception
