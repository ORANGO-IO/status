import requests

def alembic_version(url):
    response =requests.get(url, )
    if response.status_code == 200:
        json = response.json()
        print(json)
        if json and json['alembic_version']:
            return True 
        return False
    return False
