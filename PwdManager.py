import requests
from cryptography.fernet import Fernet

import os
import json

url = "http://127.0.0.1:8000"
id = 0

api_key = "U4ZJ4ZycAxtiZHQ4cnkorU-Mh_wNNfQV8B0tlbvwgMM="

with open(os.path.join("API", "JSON", "return_calls.json"), "r") as f:
    return_calls: dict = json.load(f)

success_calls = return_calls["success"]
error_calls = return_calls["errors"]


while True:
    print("------------------------------------------------------\n")
    cmd = input(
        "Instructions- \nC - create a password \nV - View a password\nU - Update a password\nD - Delete a password\nE - Exit the program\nEnter your commmand:"
    )

    if cmd.upper() == "C":
        print("------------------------------------------------------\n")
        id = input("Enter an id: ")
        response = requests.get(url=url + "/check-id?id=" + str(id)).json()
        if response != error_calls["idNotFound"]:
            print("ID does not exist")
            continue
        user = input("Username: ")
        pwd = input("Password: ")
        website = input("Website: ")
        response = requests.post(
            url=url + "/create-pwd?id=" + str(id) + "&api_key=" + api_key,
            json={
                "user": user,
                "pwd": pwd,
                "website": website,
            },
        )
        if response != error_calls["passwordAlreadyExists"]:
            print(
                "------------------------------------------------------\nSuccess! Password created!"
            )
        else:
            print("Password already exists")

    elif cmd.upper() == "V":
        id = input("Enter an id: ")
        response = requests.get(url=url + "/check-id?id=" + str(id)).json()
        print(response)
        if response == error_calls["idNotFound"]:
            print("ID does not exist")
            continue

        pwd = requests.get(
            url + "/get-pwd?id=" + str(id) + "&api_key=" + api_key
        ).json()

        if pwd != error_calls["idNotFound"]:
            user = pwd["user"]
            pwwd = pwd["pwd"]
            website = pwd["website"]
        else:
            print("Password ID does not exist")

        print(
            "------------------------------------------------------\n" "User: " + user,
            "\nPassword: "
            + pwwd
            + "\nWebsite: "
            + website
            + "\n------------------------------------------------------\n",
        )
    elif cmd.upper() == "U":
        id = input("Enter an id: ")
        response = requests.get(url=url + "/check-id?id=" + str(id)).json()
        if response == error_calls["idNotFound"]:
            print("ID does not exist")
            continue
        else:
            pass
        pwd = input("Enter the new password: ")
        response = requests.put(
            url=url
            + "/update-pwd?id="
            + str(id)
            + "&api_key="
            + api_key
            + "&pwd="
            + pwd,
        )
        if response == error_calls["idNotFound"]:
            print("Password ID does not exist")
        else:
            print(
                "Success! Password updated!\n------------------------------------------------------\n"
            )
    elif cmd.upper() == "D":
        id = input("Enter an id: ")
        response = requests.get(url=url + "/check-id?id=" + str(id)).json()
        if response == error_calls["idNotFound"]:
            print("ID does not exist")
            continue
        else:
            pass
        request = requests.delete(url=url + "/delete-pwd?id=" + str(id))
        if request == error_calls["passwordDeleted"]:
            print("Password ID does not exist")
        else:
            print(
                "Success! Password deleted!\n------------------------------------------------------\n"
            )
    elif cmd.upper() == "E":
        print("Bye!")
        break
        quit()
    else:
        print("INVALID COMMAND!")
        continue
