from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserModel, RestaurantModel, ReservationModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

def send_email_notification(to_email: str, subject: str, body: str):
    """Send email notification using SMTP"""
    try:
        # Email configuration
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_username = os.getenv("SMTP_USERNAME")
        smtp_password = os.getenv("SMTP_PASSWORD")
        from_email = os.getenv("FROM_EMAIL")

        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Add body
        msg.attach(MIMEText(body, 'html'))

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

@router.post("/send-booking-confirmation/{reservation_id}")
async def send_booking_confirmation(
    reservation_id: int,
    db: Session = Depends(get_db)
):
    try:
        # Get reservation details
        reservation = db.query(ReservationModel.Reservation).filter(
            ReservationModel.Reservation.reservation_id == reservation_id
        ).first()
        
        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")

        # Get restaurant details
        restaurant = db.query(RestaurantModel.Restaurant).filter(
            RestaurantModel.Restaurant.restaurant_id == reservation.restaurant_id
        ).first()

        # Get customer email
        customer = db.query(UserModel.User).join(
            UserModel.User.customer
        ).filter(
            UserModel.User.user_id == reservation.customer.user_id
        ).first()

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Create email content
        subject = f"Booking Confirmation - {restaurant.name}"
        body = f"""
        <html>
            <body>
                <h2>Booking Confirmation</h2>
                <p>Dear {customer.first_name},</p>
                <p>Your table has been successfully booked at {restaurant.name}.</p>
                <h3>Booking Details:</h3>
                <ul>
                    <li>Restaurant: {restaurant.name}</li>
                    <li>Date: {reservation.reservation_time.strftime('%Y-%m-%d')}</li>
                    <li>Time: {reservation.reservation_time.strftime('%H:%M')}</li>
                    <li>Party Size: {reservation.party_size}</li>
                    <li>Confirmation Code: {reservation.confirmation_code}</li>
                </ul>
                <p>Special Requests: {reservation.special_requests or 'None'}</p>
                <p>Restaurant Address: {restaurant.address_line1}, {restaurant.city}, {restaurant.state} {restaurant.zip_code}</p>
                <p>Restaurant Phone: {restaurant.phone_number}</p>
                <p>Thank you for choosing BookTable!</p>
            </body>
        </html>
        """

        # Send email
        if send_email_notification(customer.email, subject, body):
            return {"message": "Booking confirmation email sent successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to send email")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))