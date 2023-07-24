from fastapi import FastAPI
from routes.note import app
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


App = FastAPI()
App.mount("/static", StaticFiles(directory="static"), name="static")

App.include_router(app)