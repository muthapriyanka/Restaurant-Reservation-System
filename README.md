# Restaurant Booking App

> A full-stack reservation platform with role-based UX for Customers, Business Owners, and Admins.

## 📝 Project Overview
A multi-role (Customer, BusinessOwner, Admin) booking system built with:
- **Backend**: FastAPI + MySQL  
- **Frontend**: ReactJS  
- **Hosting**: AWS, GCP(For Database)  

---

## 🚀 Feature Set

- **Customer**  
  - Search restaurants by date/time/party size & location  
  - View real-time availability slots  
  - Book, view, cancel reservations  
  - Submit and read reviews  

- **Restaurant Manager**  
  - CRUD restaurant listings (details, operating hours, photos)  
  - Manage table configurations & capacities   

- **Admin**  

  - Approve/reject new listings  
  - Monitor usage analytics  
  - Manage users & listings  

---

## Deployment Notes

This project was previously deployed on AWS using Terraform for development and demo purposes. The AWS resources are not currently running because keeping the cloud infrastructure active would incur ongoing cost.

For a low-cost public demo, use the `render-postgres-deploy` branch. That branch includes a Render Blueprint (`render.yaml`) for:

- FastAPI backend on Render Web Service
- React frontend on Render Static Site
- Render Postgres database

Render's free Postgres option is useful for demos, but it has limits: one free database per workspace, 1 GB storage, no backups, and expiration after 30 days. If Render changes the generated service URLs, update these environment variables in the Render dashboard:

- Backend: `CORS_ORIGINS`
- Frontend: `REACT_APP_API_BASE_URL`

The backend expects `DATABASE_URL` to point to a PostgreSQL database in this branch.


  <img width="1134" height="825" alt="Screenshot 2025-05-12 at 11 19 28 AM" src="https://github.com/user-attachments/assets/056de593-6fbf-414c-aca2-350f5c61bbe0" />

  

  <img width="1457" height="821" alt="Screenshot 2025-05-12 at 11 46 18 AM" src="https://github.com/user-attachments/assets/9ce745ea-fe8c-467b-ad24-1671a6bfc731" />

  <img width="1457" height="854" alt="Screenshot 2025-05-12 at 11 47 53 AM" src="https://github.com/user-attachments/assets/bf379f0b-c3c2-4bad-a349-5964507743b2" />

  

