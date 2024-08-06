import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.routers import router as task_router

logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up.")
    # await create_tables()
    yield
    # await delete_tables()
    logger.info("Shutting down.")


app = FastAPI(lifespan=lifespan)

app.include_router(router=task_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
