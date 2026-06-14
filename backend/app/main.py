import os

from fastapi import FastAPI
from app.routes import email  # Add this import
from fastapi.middleware.cors import CORSMiddleware
from app.auth.auth_middleware import AuthMiddleware
from app.routes import (
    customerreviews,
    operatinghours,
    photos,
    reservation,
    reservationslots,
    restaurant,
    table,
    user,
)

DEFAULT_CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://3.101.252.93:3000",
]


def get_cors_origins():
    origins = os.getenv("CORS_ORIGINS")
    if not origins:
        return DEFAULT_CORS_ORIGINS
    return [origin.strip() for origin in origins.split(",") if origin.strip()]


app = FastAPI(
    title="FastAPI Backend",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)
app.add_middleware(AuthMiddleware)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(user.router, prefix="/api", tags=["Users"])
app.include_router(restaurant.router, prefix="/api", tags=["Restaurants"])
app.include_router(operatinghours.router, prefix="/api", tags=["Operating Hours"])
app.include_router(table.router, prefix="/api", tags=["Tables"])
app.include_router(reservationslots.router, prefix="/api", tags=["Reservation Slots"])
app.include_router(customerreviews.router, prefix="/api", tags=["Customer Reviews"])
app.include_router(reservation.router, prefix="/api", tags=["Reservations"])
app.include_router(photos.router, prefix="/api", tags=["Photos"])
app.include_router(email.router, prefix="/api", tags=["email"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
