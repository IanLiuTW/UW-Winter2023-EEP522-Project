import uvicorn
from fastapi import FastAPI
from server_health_check import server_health_check
from sftp_manager import sftp_manager

app = FastAPI()

# This endpoint is used to test the server
@app.get("/")
def read_root():
    return {"Hello": "World!"}

# Include the routers to the app
app.include_router(server_health_check.router, prefix='/server_health_check')
app.include_router(sftp_manager.router, prefix='/sftp_manager')

# Run the app
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")