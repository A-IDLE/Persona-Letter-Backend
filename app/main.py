from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
from pathlib import Path
from api.endpoints.write_letter import router
from models.database import init_db
from models import *
from services.others.setup import character_setup_by_names
# from api.routers.routers import router

fastapi_app = FastAPI()

# Initialize the database
init_db()  # Call init_db to create the database tables at startup

# Mount the router
fastapi_app.include_router(router)

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


# characters_names = [
#     "Harry Potter",
#     "Hermione Granger",
#     "Ron Weasley",
#     "Albus Dumbledore",
#     "Severus Snape",
#     "Sirius Black",
#     "Luna Lovegood",
#     "Rubeus Hagrid",
#     "Voldemort",
#     "Dobby",
#     "Ginny Weasley"
# ]


# character_setup_by_names(characters_names)


if __name__ == "__main__":
    uvicorn.run('main:fastapi_app',
                host='localhost', port=9000, reload=True)