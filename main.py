from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl
from contextlib import asynccontextmanager
import time
import os
from sqlalchemy.orm import Session

import secrets
import string

from database import engine, SessionLocal, Base
from models import URL

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):

    for _ in range(10):

        try:
            Base.metadata.create_all(bind=engine)
            print("Database connected.")
            break

        except Exception:
            print("Database not ready yet...")
            time.sleep(2)

    yield


app = FastAPI(lifespan=lifespan)

ALPHABET = string.ascii_letters + string.digits
SLUG_LENGTH = 6

# Serve static files (frontend)
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class ShortenRequest(BaseModel):
    url: HttpUrl


def generate_slug(db: Session):

    while True:

        slug = "".join(
            secrets.choice(ALPHABET)
            for _ in range(SLUG_LENGTH)
        )

        existing_slug = (
            db.query(URL)
            .filter(URL.slug == slug)
            .first()
        )

        if not existing_slug:
            return slug


@app.get("/")
def home():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    return {
        "message": "URL Shortener API running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/shorten")
def shorten_url(body: ShortenRequest):

    db = SessionLocal()

    existing_url = (
        db.query(URL)
        .filter(URL.url == str(body.url))
        .first()
    )

    if existing_url:

        db.close()

        return {
            "short_code": existing_url.slug,
            "url": existing_url.url,
            "clicks": existing_url.clicks
        }

    slug = generate_slug(db)

    new_url = URL(
        slug=slug,
        url=str(body.url)
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    db.close()

    return {
        "short_code": new_url.slug,
        "url": new_url.url,
        "clicks": new_url.clicks
    }


@app.get("/stats/{slug}")
def slug_stats(slug: str):

    db = SessionLocal()

    url_data = (
        db.query(URL)
        .filter(URL.slug == slug)
        .first()
    )

    if not url_data:

        db.close()

        raise HTTPException(
            status_code=404,
            detail="Slug not found"
        )

    response = {
        "short_code": url_data.slug,
        "url": url_data.url,
        "clicks": url_data.clicks
    }

    db.close()

    return response


@app.get("/{slug}")
def redirect_slug(slug: str):

    db = SessionLocal()

    url_data = (
        db.query(URL)
        .filter(URL.slug == slug)
        .first()
    )

    if not url_data:

        db.close()

        raise HTTPException(
            status_code=404,
            detail="Slug not found"
        )

    url_data.clicks += 1

    db.commit()

    redirect_url = url_data.url

    db.close()

    return RedirectResponse(
        url=redirect_url
    )
