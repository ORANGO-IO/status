import requests

def alembic_version(self,url):
    response =requests.get(url)
    if response.status_code == 200:
        json = response.json()
        if json.alembic_version:
            return True 
        return False
    return False
