from models.note import Note
from config.db import conn
from schemas.noteSchema import noteEntity, notesEntity
from fastapi import FastAPI, Request, HTTPException, Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


app = APIRouter()
templates = Jinja2Templates(directory="templates")

db = conn['Notes']
collection = db['note']

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        return templates.TemplateResponse('index.html', {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/notes", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        docs = collection.find({})

        notes = []
        for doc in docs:
            notedict = {'title': doc['title'], 'content': doc['content'],'important':doc['important']}

            notes.append(notedict)

        return templates.TemplateResponse('item.html', {"request": request,"docs":notes})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class NoteResponse(BaseModel):  # Define the response model
    message: str


@app.post('/submit', response_model=NoteResponse)  # Use the response model here
async def add_note(
    request: Request,  # Add the Request object as a parameter

):
    try:
        form = await request.form()


        form_dict = {k: v for k, v in form.items()}

        note= collection.insert_one(form_dict)

        return RedirectResponse(url="/notes", status_code=303)


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class NoteResponse1(BaseModel):  # Define the response model
    message: str

# ... your other FastAPI routes ...
@app.post('/delete', response_model=NoteResponse1)
async def delete_note(request: Request):
    try:
        formData = await request.form()
        formData_dict = {}



        for key in formData.items():
            formData_dict[key[0]] = key[1]

        note = collection.delete_many(formData_dict)

        # Create a response using the NoteResponse model
        return RedirectResponse(url="/notes", status_code=303)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

