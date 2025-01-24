# API for Password Managment System

# Used to store passwords

# Importing modules for API functioning
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from pwd_class import pwd
from cryptography.fernet import Fernet

# Importing modules for API running and file loading
import uvicorn
import json
import os


app = FastAPI()

# Opening all json files
with open(
    os.path.join("API", "JSON", "pwds.json"),
    "r",
) as f:
    pwds: dict = json.load(f)
    ids: list = list(pwds.keys())
    print(ids)

with open(os.path.join("API", "JSON", "return_calls.json"), "r") as f:
    return_calls: dict = json.load(f)

success_calls = return_calls["success"]
error_calls = return_calls["errors"]


# Home link which shows all other links
@app.get("/")
def home():
    return {
        "Welcome": "To the Password Manager API",
        "Author": "Mathdallas",
        "Commands": {
            "Generate a key": "http://127.0.0.1:8000/generate-key",
            "View existing keys": "http://127.0.0.1:8000/view-key",
            "Get Password": "http://127.0.0.1:8000/get-pwd?id=AN ID THAT EXISTS",
            "Get All Passwords": "http://127.0.0.1:8000/get-all-pwds",
            "Create Password": "http://127.0.0.1:8000/create-pwd?id=A UNIQUE ID WHICH DOESN'T EXIST",
            "Update Password": "http://127.0.0.1:8000/update-pwd?id=AN ID THAT EXISTS",
            "Delete Password": "http://127.0.0.1:8000/delete-pwd?id=AN ID THAT EXISTS",
        },
        "Documentation": "http://127.0.0.1:8000/docs",
    }


# Generates a key to encrypt and decrypt passwords
@app.get("/generate-key")
def generate_pwd():
    with open(os.path.join("API", "pwd_key.txt"), "w+") as f:
        if f.read() == "":
            key = Fernet.generate_key()
            f.write(key.decode())
            return {str(key)}

        return error_calls["key_exists"]


# Views the current key used
@app.get("/view_key")
def view_pwd():
    with open(os.path.join("API", "pwd_key.txt"), "r") as f:
        if f.read() != "":
            return f.read()
        else:
            return


# Checks if the given id is in the present keys
@app.get("/check-id")
def check_id(id: int):
    if str(id) in ids:
        return success_calls["idExists"]
    else:
        return error_calls["idNotFound"]


# Return the password addressed to the specified ID, else returns an error
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
        return error_calls["idNotFound"]


# Creates a password and registers it if the ID does not exist.
@app.post("/create-pwd")
def create_pwd(id: str, api_key: str, password: pwd):
    key = api_key.encode()
    cipher_suite = Fernet(key=key)
    if id in pwds:
        return error_calls["passwordAlreadyExists"]

    pwds[id] = {
        "user": cipher_suite.encrypt(password.user.encode()).decode(),
        "pwd": cipher_suite.encrypt(password.pwd.encode()).decode(),
        "website": cipher_suite.encrypt(password.website.encode()).decode(),
    }
    with open(os.path.join("API", "JSON", "pwds.json"), "w") as f:
        json.dump(pwds, f)
        f.close()
    return success_calls["passwordCreated"]


# Updates a password's password if the password is there, else return error
@app.put("/update-pwd")
def update_pwd(id: int, api_key: str, pwd: str):
    key = api_key.encode()
    cipher_suite = Fernet(key=key)
    if str(id) in pwds:
        pwds[str(id)]["pwd"] = cipher_suite.encrypt(pwd.encode()).decode()
        with open(os.path.join("API", "JSON", "pwds.json"), "w") as f:
            json.dump(pwds, f)
            f.close()
        success_calls["passwordUpdated"]
    else:
        error_calls["idNotFound"]


# Deletes a password if the password is existing, else returns error
@app.delete("/delete-pwd")
def delete_pwd(id: int):
    if id in pwds:
        del pwds[id]
        with open(os.path.join("API", "JSON", "pwds.json"), "w") as f:
            json.dump(pwds, f)
            f.close()
        success_calls["passwordDeleted"]
    else:
        error_calls["passwordAlreadyDeleted"]


uvicorn.run(app=app)
