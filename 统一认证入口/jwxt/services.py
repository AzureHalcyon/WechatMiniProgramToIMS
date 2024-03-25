import requests
from database import SessionLocal
from sqlalchemy.orm import Session
from requests.utils import dict_from_cookiejar
from lxml import etree

from .models import UserCookies
from utils.getHeader import jwxtHedaer
from utils.getUrl import myActionUrl


def checkJwxtCookies(cookies: dict) -> bool:
    try:
        session = requests.Session()
        sessionCookies = requests.cookies.RequestsCookieJar()
        for key, value in cookies.items():
            sessionCookies.set(key, value)
        session.cookies.update(sessionCookies)
        response = session.get(myActionUrl, headers=jwxtHedaer)  # 请求个人信息

        tree = etree.HTML(response.text)
        UserInfoTableElements = tree.xpath('//*[@id="user-info"]/div/div[2]/table')
        if UserInfoTableElements:
            info_table_html = etree.tostring(UserInfoTableElements[0], method='html', pretty_print=True,
                                             encoding='utf-8').decode('utf-8')
            print(info_table_html)
            return True
        else:
            return False
    except:
        return False


def getJwxtCookieFromTicketUrl(TicketUrl: str) -> tuple[bool, dict]:
    try:
        session = requests.Session()
        response = session.get(TicketUrl, headers=jwxtHedaer)
        return True, dict_from_cookiejar(session.cookies)
    except Exception as e:
        return False, str(e)
