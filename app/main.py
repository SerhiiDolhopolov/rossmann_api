import uvicorn
from fastapi import FastAPI

from app.api.categories import router as categories_router
from app.api.products import router as products_router


app = FastAPI()
app.include_router(categories_router)
app.include_router(products_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)