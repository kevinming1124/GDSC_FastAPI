from fastapi import FastAPI
from database.generic import init_db
from setting.config import get_settings

settings = get_settings()
app = FastAPI()
    
if settings.run_mode == "ASYNC":
    from api.infor import router as infor_router
    from api.users import router as user_router
    from api.items import router as item_router
    from database.generic import init_db , close_db

    app.include_router(infor_router)
    app.include_router(user_router)
    app.include_router(item_router)

    @app.on_event("startup")
    async def startup():
        await init_db()

    @app.on_event("shutdown")
    async def shutdown():
        await close_db()
else:
    from sync.api.infor import router as infor_router
    from sync.api.users import router as user_router
    from sync.api.items import router as item_router
    from sync.database.generic import init_db , close_db

    app.include_router(infor_router)
    app.include_router(user_router)
    app.include_router(item_router)
    

    @app.on_event("startup")
    def startup():
        init_db()

    @app.on_event("shutdown")
    def shutdown():
        close_db()





