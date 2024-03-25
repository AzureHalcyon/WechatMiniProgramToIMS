import requests
from lxml import etree
from utils.encrypt import encryptAes
from utils.getHeader import loginHeader, jwxtHedaer
from urllib.parse import quote
import re
from requests.utils import dict_from_cookiejar

url = 'https://ids.neuq.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.neuq.edu.cn%2Feams%2FhomeExt.action'
session = requests.Session()
response = session.get(url, headers=loginHeader)
tree = etree.HTML(response.content)
pwdDefaultEncryptSalt = tree.xpath('//*[@id="pwdDefaultEncryptSalt"]')[0].get('value')
lt_val = tree.xpath('//*[@id="casLoginForm"]/input[1]')[0].get('value')
execution = tree.xpath('//*[@id="casLoginForm"]/input[3]')[0].get('value')

form_data = {
    'username': '202113375',
    'password': encryptAes("Snowgongzuoshi2.", pwdDefaultEncryptSalt),
    'lt': lt_val,
    'dllt': 'userNamePasswordLogin',
    'execution': execution,
    '_eventId': 'submit',
    'rmShown': '1'
}
response = session.post(url, headers=loginHeader, data=form_data, allow_redirects=False)
# print(str(session.cookies))
# redirects_url = re.findall('<a href="(.*?)">http',response.text,re.S)[0]
# session = requests.Session()
# response = session.get(redirects_url,headers = jwxtHedaer,allow_redirects=False)
jwxtBaseUrl = response.headers['location']  # ticket=ST-.. 获取jwxt子系统凭证
# print(jwxtBaseUrl)
session1 = requests.Session()
response = session1.get(jwxtBaseUrl, headers=jwxtHedaer)  # 获取jwxt的Cookies
print(dict_from_cookiejar(session1.cookies))
myUserUrl = 'https://jwxt.neuq.edu.cn/eams/security/my.action'
response = session1.get(myUserUrl, headers=jwxtHedaer)  # 请求个人信息
# 应该保存此cookies

tree = etree.HTML(response.text)
info_table_elements = tree.xpath('//*[@id="user-info"]/div/div[2]/table')
info_table_html = etree.tostring(info_table_elements[0], method='html', pretty_print=True, encoding='utf-8').decode(
    'utf-8')
print(info_table_html)
