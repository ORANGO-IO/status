from sqlalchemy import create_engine

def database_connection(url):
    try:
        create_engine(url)
        return True               
    except:
        return False