from getopt import getopt
from re import search
from sys import argv
from urllib.parse import urlencode
from urllib.request import urlopen

Username: str = None
Password: str = None
ServerIP: str = None
TestAddress: str = None


def getServerIP():
    try:
        page = urlopen(TestAddress, timeout=5).read().decode('gb2312')
        match_obj = search(r"v4serip='(.*?)'", page)
        rst = match_obj.group(1)
        print('自动获得服务器IP: ' + rst)
        return rst
    except:
        print('自动获取服务器IP失败')
        print('尝试使用119.39.119.2')
        return '119.39.119.2'


def login():
    if Username is None or Password is None:
        print('登录的帐号密码是必需的')
        print('用法: python3 csu-drcom.py login -u 帐号 -p 密码')
        exit(1)
    host = 'http://' + ServerIP + '/'
    content = {
        'DDDDD': Username,
        'upass': Password
    }
    if not content['DDDDD'].endswith('@zndx'):
        content['DDDDD'] += '@zndx'

    result: str
    try:
        result = urlopen(host, urlencode(content).encode('utf-8'), timeout=10).read().decode('gb2312')
    except TimeoutError:
        print('登录超时')
        exit(-1)
    if 'Msg=' in result:
        print('登录信息：')
        print(getMsg(result))
    else:
        print('登录成功！(大概')


def logout():
    host = 'http://' + ServerIP + '/F.htm'
    result: str
    try:
        result = urlopen(host, timeout=10).read().decode('gb2312')
    except TimeoutError:
        print('注销超时')
        exit(-1)
    print(getMsg(result))


def getMsg(resultPage: str):
    msg = int(search(r'Msg=(\d*)', resultPage).group(1))
    if msg == 0 or msg == 1:
        msga = search(r"msga='(.*?)'", resultPage).group(1)
        if msg == 1 and msga != '':
            if msga == 'error0':
                return '本IP不允许Web方式登录'
            elif msga == 'error1':
                return '本账号不允许Web方式登录'
            elif msga == 'error2':
                return '本账号不允许修改密码'
            else:
                return msga
        else:
            return '账号或密码不对，请重新输入'
    elif msg == 2:
        return '该账号正在使用中，请您与网管联系'
    elif msg == 3:
        return '本账号只能在指定地址使用'
    elif msg == 4:
        return '本账号费用超支或时长流量超过限制'
    elif msg == 5:
        return '本账号暂停使用'
    elif msg == 6:
        return 'System buffer full'
    elif msg == 7:
        return ''
    elif msg == 8:
        return '本账号正在使用,不能修改'
    elif msg == 9:
        return '新密码与确认新密码不匹配,不能修改'
    elif msg == 10:
        return '密码修改成功'
    elif msg == 11:
        return '本账号只能在指定地址使用'
    elif msg == 14:
        time = search(r"time='(.*?)'", resultPage).group(1).strip()
        flow = str(float(search(r"flow='(.*?)'", resultPage).group(1).strip()) / 1024)
        return '注销成功\n已使用时间：' + time + ' Min\n已使用流量：' + flow + ' MByte'
    elif msg == 15:
        return '登录成功'
    return resultPage


if __name__ == '__main__':
    if len(argv) < 2 or argv[1] != 'login' and argv[1] != 'logout':
        print('用法：')
        print('    登录：')
        print('        python3 csu-drcom.py login -u 帐号 -p 密码')
        print('        python3 csu-drcom.py login -u 帐号 -p 密码 -s 服务器IP')
        print('        python3 csu-drcom.py login -u 帐号 -p 密码 --test-address 用于探测服务器IP的网址')
        print('    注销：')
        print('        python3 csu-drcom.py logout')
        print('        python3 csu-drcom.py logout -s 服务器IP')
        print()
        print('说明：')
        print('    当前中南大学南校服务器IP为119.39.119.2')

        exit(0)

    optlist = dict(getopt(argv[2:], 'u:p:s:', ['test-address='])[0])
    Username = optlist.get('-u')
    Password = optlist.get('-p')
    TestAddress = optlist.get('--test-address', 'http://example.com/')
    if '-s' in optlist:
        ServerIP = optlist['-s']
    else:
        ServerIP = getServerIP()

    if argv[1] == 'login':
        login()
    elif argv[1] == 'logout':
        logout()
