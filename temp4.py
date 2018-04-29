import requests
import re
from PIL import Image
from bs4 import BeautifulSoup
import pytesseract
from lxml import etree
session=requests.session()
cookiejars=""
headers={
    'Host':'rz.wzu.edu.cn',
     'Origin':'http://rz.wzu.edu.cn',
     'Referer':'http://rz.wzu.edu.cn/zfca/login',
     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
}

def get_photonumble():#获取验证码，由于是session,所以完全可以使用这个，不用担心验证码和其他的不准确性。
    code = session.get('http://rz.wzu.edu.cn/zfca/captcha.htm')
    with open("D://1.jpg", 'wb') as f:
        f.write(code.content)
        f.close()
    im = Image.open("D://1.jpg")
    text = pytesseract.image_to_string(im)
    return text

def login(numble,user,pwd):#用户登录
    global cookiejars
    postdata = {
        "username": user,
        "password": pwd,
        "useValidateCode": "1",
        "isremenberme": "1",
        "ip": " ",
        'lt': '',
        '_eventId': 'submit',
        'losetime': '30',
        'j_captcha_response': numble,
        'rememberMe': 'true'
    }
    login_page=session.get('http://rz.wzu.edu.cn/zfca/login',headers=headers)
    soup=BeautifulSoup(login_page.text,'lxml')
    soup=soup.find(attrs={'name':'lt'})
    postdata['lt']=soup['value']
    session.post('http://rz.wzu.edu.cn/zfca/login',data=postdata,headers=headers)
    page=session.get('http://portal.wzu.edu.cn/portal.do?caUserName=17211134120').text

    cookiejars=session.cookies

    page=BeautifulSoup(page,'html.parser')
    try:
        ans = page.find('title').string
        name = page.find('em').string.split(': ')[-1]

        return [ans,name]
    except:
        return ['none','none']
def getmessage(user,name):#获取个人信息里面的东西

    headers['Referer'] = 'http://jwc3.wzu.edu.cn/xs_main.aspx?xh=%s&type=1' % (user)
    headers['Host'] = 'jwc3.wzu.edu.cn'
    headers['Upgrade-Insecure-Requests'] = '1'
    Cookies = {'ASP.NET_SessionId': 'daiexo55x45kyz45cmhd2crs'}
    for key, value in cookiejars.items():
        Cookies[key] = value
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    url = 'http://jwc3.wzu.edu.cn/xsgrxx.aspx?xh=%s&xm=%s&gnmkdm=N121501' % (user, name)
    page = session.get(url, headers=headers, cookies=Cookies)#这里是获取个人信息，由于不知道要什么信息，所以先以message的信息存储。
    page=BeautifulSoup(page.text,'html.parser')
    get_userphoto(user)
def get_userphoto(user):#获取user对应的图片
    Cookie = {'ASP.NET_SessionId': 'daiexo55x45kyz45cmhd2crs'}
    r = session.get('http://192.168.10.3/xgxt/xsxx_xsgl.do?method=showPhoto&xh=%s' % (user))
    if len(r.content) > 10000:
        root = 'E://pt/%s.jpeg' % (user)
        with open(root, 'wb+') as f:
            f.write(r.content)
            f.close()
    im = Image.open(root)#弹出图片
    im.show()
def process():
    user=input("学号：")
    pwd=input("密码：")

    for i in range(3):#进行三次登录,如果不行就说明失败
        numble = get_photonumble()
        anss = login(numble, user, pwd)
        ans = anss[0]
        name = anss[1]
        if re.findall("个人门户", ans):
            print("登录成功")
            getmessage(user, name)
            break
        else:
            print("failed")

if __name__ == '__main__':
    process()


