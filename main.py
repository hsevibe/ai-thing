import uvicorn
from router import router

if __name__ == "__main__":
    uvicorn.run(router, host="0.0.0.0", port=8000)
