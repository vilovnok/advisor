from fastapi import FastAPI
from .api.routers import all_routers
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title='Advisor')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in all_routers:
    app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)