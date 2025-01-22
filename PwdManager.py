import requests
from cryptography.fernet import Fernet

url = "http://127.0.0.1:8000"
id = 0

api_key = "U4ZJ4ZycAxtiZHQ4cnkorU-Mh_wNNfQV8B0tlbvwgMM="

while True:
    print("------------------------------------------------------\n")
    cmd = input(
        "Instructions- \nC - create a password \nV - View a password\nU - Update a password\nD - Delete a password\nE - Exit the program\nEnter your commmand:"
    )

    if cmd.upper() == "C":
        print("------------------------------------------------------\n")
        user = input("Username: ")
        pwd = input("Password: ")
        website = input("Website: ")
        requests.post(
            url=url + "/create-pwd?id=" + str(id) + "&api_key=" + api_key,
            json={
                "user": user,
                "pwd": pwd,
                "website": website,
            },
        )
        id += 1
        print(
            "------------------------------------------------------\nSuccess! Password created!"
        )

    elif cmd.upper() == "V":
        id = input("Enter an id: ")
        pwd = requests.get(
            url + "/get-pwd?id=" + str(id) + "&api_key=" + api_key
        ).json()

        user = pwd["user"]
        pwwd = pwd["pwd"]
        website = pwd["website"]

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
        pwd = input("Enter the new password: ")
        requests.put(
            url=url
            + "/update-pwd?id="
            + str(id)
            + "&api_key="
            + api_key
            + "&pwd="
            + pwd,
        )
        print(
            "Success! Password updated!\n------------------------------------------------------\n"
        )
    elif cmd.upper() == "D":
        id = input("Enter an id: ")
        requests.delete(url=url + "/delete-pwd?id=" + str(id))
    elif cmd.upper() == "E":
        print("Bye!")
        break
        quit()
    else:
        print("INVALID COMMAND!")
        continue
