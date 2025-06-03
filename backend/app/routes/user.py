from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm

# from app.auth.auth_middleware import AuthMiddleware
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import database
from app.auth.jwt_utils import create_access_token
from app.models import AdminModel, CustomerModel, RestaurantManagerModel, UserModel
from app.schemas import UserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    # Inline query to retrieve the user by email (using the username field)
    user = (
        db.query(UserModel.User)
        .filter(UserModel.User.email == form_data.username)
        .first()
    )
    # Verify password using the password context
    if not user or not pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(
        data={"user_id": user.user_id, "email": user.email, "role": user.role.value}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserSchema.UserResponse)
def register_user(user: UserSchema.UserCreate, db: Session = Depends(database.get_db)):
    # Check if a user with the same email already exists
    existing_user = (
        db.query(UserModel.User).filter(UserModel.User.email == user.email).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the provided password
    hashed_password = pwd_context.hash(user.password)
    # Create a new User instance with the hashed password
    new_user = UserModel.User(
        email=user.email,
        password_hash=hashed_password,
        phone_number=user.phone_number,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create an entry in the respective table based on the user's role
    if user.role.name == "CUSTOMER":  # or use UserRole.CUSTOMER.name if imported
        new_customer = CustomerModel.Customer(
            user_id=new_user.user_id,
            notification_preference=CustomerModel.NotificationPreference.EMAIL,  # default value
        )
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
    elif user.role.name == "ADMIN":  # or UserRole.ADMIN.name
        new_admin = AdminModel.Admin(user_id=new_user.user_id)
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
    elif user.role.name == "RESTAURANT_MANAGER":  # or UserRole.RESTAURANT_MANAGER.name
        new_manager = RestaurantManagerModel.RestaurantManager(
            user_id=new_user.user_id,
            approved_at=None,  # default value
        )
        db.add(new_manager)
        db.commit()
        db.refresh(new_manager)

    return new_user


@router.get("/users/{user_id}", response_model=UserSchema.UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(database.get_db)):
    # Inline query to fetch the user by user_id
    db_user = db.query(UserModel.User).filter(UserModel.User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/protected-route")
async def protected_route(request: Request):
    user = request.state.user
    return {"message": f"Hello, {user['email']} with role {user['role']}"}
