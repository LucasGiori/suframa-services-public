import requests,requests.utils
import json
import urllib3

url = 'https://simnac.suframa.gov.br/'
url_login = 'https://appsimnac.suframa.gov.br/Login?'
session = requests.session()


def login(login,senha):    
    try:        
        urllib3.disable_warnings()
        login=session.get('https://appsimnac.suframa.gov.br/Login?usuario='+str(login)+'&senha='+str(senha),verify=False)
        token_security = json.loads(login.text)["token"]
        return session,token_security
    except:
        return session,''

def exitSession(session):
    urllib3.disable_warnings()
    session.get('https://appsimnac.suframa.gov.br/logout')


