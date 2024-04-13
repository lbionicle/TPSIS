from fastapi import FastAPI, HTTPException, Depends
from fastapi.params import Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Type
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    def __init__(self, db: Session):
        self.db = db
    def save(self):
        get_user(self.id).update(self)

    id: int
    username: str
    email: str
    age: int
    name: str
    password: str
    phone: str
    is_admin: bool

class ObjectFactory:

  def __init__(self, db: Session):
   self.db = db

  def get_object(self, model_type: Type[BaseModel]) -> BaseModel:
    if model_type is User:
      return User(self.db)
    elif model_type is Office:
      return Office(self.db)

class Office(BaseModel):
    id: int
    name: str
    address: str

class Application(BaseModel):
    id: int
    user_id: int
    office_id: int
    status: str

users = []
offices = []
applications = []

def get_user(db: Session, user_id: int):
  return db.query(User).filter(User.id == user_id).first()

def get_office(db: Session, office_id: int):
  return db.query(Office).filter(Office.id == office_id).first()

def check_user(users, user):
    if any(u for u in users if u.username == user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    return True

def validate_credentials(username, password):
    user = next((u for u in users if u['username'] == username and u['password'] == password), None)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

def find_user(users, id):
    return next((u for u in users if u['id'] == id), None)

def find_office(offices, id):
    return next((o for o in offices if o['id'] == id), None)

def validate_admin(users, id):
    admin = find_user(users, id)
    if admin is None or not admin['is_admin']:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin
@app.post("/register")
def register(user: User):
    check_user(users, user)
    users.append(user.dict())
    return {"msg": "User registered successfully"}

@app.post("/login")
def login(username: str, password: str):
    user = validate_credentials(username, password)
    return {"msg": "Logged in successfully"}

@app.post("/search-office")
def search_office(parameters: dict):
    office_name = parameters.get('name')
    result = [office for office in offices if office.name == office_name]
    return {"offices": result}

@app.post("/fill-application")
def fill_application(data: dict):
    user = find_user(users, data['user_id'])
    office = find_office(offices, data['office_id'])
    if user is None or office is None:
        raise HTTPException(status_code=404, detail="User or office not found")
    applications.append(data)
    return {"application": data}

@app.post("/submit-application")
def submit_application(application_id: int):
    application = next((a for a in applications if a['id'] == application_id), None)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    application['status'] = 'submitted'
    return {"status": "Application submitted"}

@app.post("/ask-question")
def ask_question(question: str):
    if question.lower() == "what is the weather today?":
        return {"answer": "I'm sorry, I cannot provide real-time data as my training only includes knowledge up until 2021."}
    else:
        return {"answer": "This is a standard answer"}


@app.post("/add-to-wishlist")
def add_to_wishlist(user_id: int, office_id: int):
    user = find_user(users, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    add_to_wishlist(user, office_id)
    return {"msg": "Office added to wishlist"}

@app.post("/manage-applications")
def manage_applications(admin_id: int):
    admin = validate_admin(users, admin_id)
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    pending_applications = [app for app in applications if app['status']=='pending']
    return {"applications": pending_applications}

@app.post("/manage-offices")
def manage_offices(admin_id: int):
    admin = validate_admin(users, admin_id)
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return {"offices": offices}

@app.post("/manage-users")
def manage_users(admin_id: int):
    admin = validate_admin(users, admin_id)
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return {"users": users}

@app.post("/generate-report")
def generate_report(admin_id: int):
    admin = validate_admin(users, admin_id)
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    report = {
        "num_users": len(users),
        "num_offices": len(offices)
    }
    return {"report": report}

@app.post("/export-report")
def export_report(admin_id: int):
    admin = validate_admin(users, admin_id)
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    report = generate_report(admin_id)
    report_data = "\n".join(f"{key}: {value}" for key, value in report['report'].items())
    return {"file": report_data}
