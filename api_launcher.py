import uvicorn

from api import app
from instance import TaskPoolInstance

if __name__ == '__main__':
    TaskPoolInstance.run()
    uvicorn.run(app, host="localhost", port=8300)