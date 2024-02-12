import dotenv
import os
import requests

dotenv.load_dotenv()
host = os.environ.get("SERVER_HOST")
port = os.environ.get("SERVER_PORT")


def main():
    response = requests.get(f"http://{host}:{port}")
    print(response.content)


main()
