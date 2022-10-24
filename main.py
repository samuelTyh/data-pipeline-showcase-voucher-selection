import os
import uvicorn
from app import api


def main():
    uvicorn.run(api, host=os.environ.get("APP_SERVER_HOST"), port=int(os.environ.get("APP_SERVER_PORT")))


main()
