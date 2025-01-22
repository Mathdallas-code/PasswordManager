# API for Password Managment System

# Used to store passwords

# Key =
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from pwd_class import pwd

from cryptography.fernet import Fernet
import uvicorn
import json

with open(
    "/Users/bruger/Desktop/MyStuff/Coding/Python/Practice/PasswordManager/API/pwds.json",
    "r",
) as f:
    pwds: dict = json.load(f)
    print(pwds)

app = FastAPI()


@app.get("/")
def home():
    return {
        "Welcome": "To the Password Manager API",
        "Author": "Mathdallas",
        "Commands": {
            "Generate a key": "/generate-key",
            "View existing keys": "/view-key",
            "Get Password": "/get-pwd?id=AN ID THAT EXISTS",
            "Get All Passwords": "/get-all-pwds",
            "Create Password": "/create-pwd?id=A UNIQUE ID WHICH DOESN'T EXIST",
            "Update Password": "/update-pwd?id=AN ID THAT EXISTS",
            "Delete Password": "/delete-pwd?id=AN ID THAT EXISTS",
        },
        "Documentation": "http://127.0.0.1:8000/docs",
    }


@app.get("/generate-key")
def generate_pwd():
    with open("PasswordManager/API/pwd_key.txt", "w+") as f:
        if f.read() == "":
            key = Fernet.generate_key()
            f.write(key.decode())
            return {str(key)}

        return {"Key already exists": f.read()}


@app.get("/view_key")
def generate_pwd():
    with open("PasswordManager/API/pwd_key.txt", "r") as f:
        return f.read()


@app.get("/get-pwd")
def get_pwd(id: str, api_key: str):
    key = api_key.encode()
    cipher_suite = Fernet(key=key)
    if str(id) in pwds:
        password = pwds[str(id)]
        return {
            "user": cipher_suite.decrypt(password["user"].encode()),
            "pwd": cipher_suite.decrypt(password["pwd"].encode()),
            "website": cipher_suite.decrypt(password["website"].encode()),
        }
    else:
        return {"Error": "ID does not exist"}


@app.post("/create-pwd")
def create_pwd(id: str, api_key: str, password: pwd):
    key = api_key.encode()
    cipher_suite = Fernet(key=key)
    if id in pwds:
        return {"Error": "Password already exists"}

    pwds[id] = {
        "user": cipher_suite.encrypt(password.user.encode()).decode(),
        "pwd": cipher_suite.encrypt(password.pwd.encode()).decode(),
        "website": cipher_suite.encrypt(password.website.encode()).decode(),
    }
    with open("PasswordManager/API/pwds.json", "w") as f:
        json.dump(pwds, f)
        f.close()
    return {"Success!": "Password created!"}


@app.put("/update-pwd")
def update_pwd(id: int, api_key: str, pwd: str):
    key = api_key.encode()
    cipher_suite = Fernet(key=key)
    if str(id) in pwds:
        pwds[str(id)]["pwd"] = cipher_suite.encrypt(pwd.encode()).decode()
        with open("PasswordManager/API/pwds.json", "w") as f:
            json.dump(pwds, f)
            f.close()
        return {"Success!": "Password changed!"}
    else:
        return {"Error": "ID does not exist."}


@app.delete("/delete-pwd")
def delete_pwd(id: int):
    if id in pwds:
        del pwds[id]
        with open("PasswordManager/API/pwds.json", "w") as f:
            json.dump(pwds, f)
            f.close()
        return {"Success!": "Password deleted!"}
    else:
        return {"Error": "ID does not exist or password was already deleted"}


uvicorn.run(app=app)
