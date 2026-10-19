# Vercel and Render deployment

The frontend runs on Vercel. The FastAPI service and PostgreSQL database run on
Render.

## Render

1. In Render, create or update a Blueprint from `render.yaml` on the deployment
   branch.
2. Confirm that the Blueprint creates `restaurant-reservation-api`,
   `restaurant-reservation-db`, and the fallback Render static frontend.
3. Wait for the API deployment to finish, then verify:
   `https://restaurant-reservation-api-6djs.onrender.com/health`.

The startup command applies the database migration and seeds the demo restaurant
data before starting FastAPI. Render supplies `DATABASE_URL` from the managed
PostgreSQL database and generates `SECRET_KEY`.

## Vercel

1. Import the GitHub repository into Vercel and select the deployment branch.
2. Keep the project root as the repository root. Vercel reads `vercel.json` and
   builds the React application under `frontend/`.
3. Deploy and open the generated `vercel.app` URL.

The production frontend defaults to the Render API URL. To use a differently
named Render service, set this Vercel environment variable and redeploy:

```text
REACT_APP_API_BASE_URL=https://YOUR-API.onrender.com/api
```

The API accepts HTTPS Vercel deployment origins through `CORS_ORIGIN_REGEX`.
Local development continues to use `http://localhost:8000/api`.
