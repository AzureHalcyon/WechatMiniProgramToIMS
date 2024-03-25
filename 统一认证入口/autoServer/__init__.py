import requests

from lxml import etree
from urllib.parse import quote

from utils.encrypt import encryptAes
from utils.getHeader import loginHeader
from utils.getUrl import jwxtAuthUrl


def getJwxtTicketFromAutoServer(username, password) -> tuple[bool, str]:
    try:
        session = requests.Session()
        response = session.get(jwxtAuthUrl, headers=loginHeader)
        tree = etree.HTML(response.content)
        pwdDefaultEncryptSalt = tree.xpath('//*[@id="pwdDefaultEncryptSalt"]')[0].get('value')
        lt_val = tree.xpath('//*[@id="casLoginForm"]/input[1]')[0].get('value')
        execution = tree.xpath('//*[@id="casLoginForm"]/input[3]')[0].get('value')
        data = {
            'username': username,
            'password': encryptAes(password, pwdDefaultEncryptSalt),
            'lt': lt_val,
            'dllt': 'userNamePasswordLogin',
            'execution': execution,
            '_eventId': 'submit',
            'rmShown': '1'
        }
        response = session.post(jwxtAuthUrl, headers=loginHeader, data=data, allow_redirects=False)

        locationUrl = response.headers.get('location', '')
        if 'ticket' in locationUrl:
            return True, locationUrl
        else:
            return False, locationUrl
    except Exception as e:
        return False, str(e)
