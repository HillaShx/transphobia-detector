import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from routers.scraping import router as scraping_router
from routers.interface import router as interface_router


load_dotenv()
app = FastAPI()


@app.get("/health")
def health_test():
    return {"status": "ok"}


app.include_router(scraping_router)
app.include_router(interface_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
