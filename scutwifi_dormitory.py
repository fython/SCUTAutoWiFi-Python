#!/usr/bin/env python3
# encoding: UTF8

import urllib.request
import socket
import sys

API_URL = "https://s.scut.edu.cn:801/eportal/?c=ACSetting&a={operation}&wlanuserip={wlanuserip}&wlanacip={wlancip}&wlanacname=&redirect=&session=&vlanid=scut-student&port=&iTermType={iTermType}&protocol=https:"
API_ERRCODE_URL = "https://s.scut.edu.cn/errcode"

OPERATION_LOGIN = 'Login'
OPERATION_LOGOUT = 'Logout'

ERRCODE_USER_NO_EXIST = 'userid error1'
ERRCODE_PASSWORD_WRONG_1 = 'userid error2'
ERRCODE_PASSWORD_WRONG_2 = 'userid error3'
ERRCODE_ACCOUNT_USING = 'Authentication Fail ErrCode=85'
ERRCODE_BIND_IP_FAILED = 'Authentication Fail ErrCode=86'
ERRCODE_OUT_OF_LIMIT_SERVER = 'Authentication Fail ErrCode=94'
ERRCODE_BANNED_TIME_1 = 'Authentication Fail ErrCode=16'
ERRCODE_BANNED_TIME_2 = 'auth error80'
ERRCODE_USER_STOP_SERVICE = 'Authentication Fail ErrCode=05'
ERRCODE_USER_OUT_OF_USAGE = 'Authentication Fail ErrCode=04'
ERRCODE_TOO_MUCH_USER = 'set_onlinet error'

SUCCESS_MSG = '已经成功登录'

ITERM_TYPE_OTHER = 0
ITERM_TYPE_PC = 1
ITERM_TYPE_MOBILE = 2
ITERM_TYPE_TABLET = 3

def login(username, pwd):
    post_data = urllib.parse.urlencode({
        '0MKKey' : '123456',
        'DDDDD' : username,
        'R1' : '0',
        'R2' : '',
        'R6' : '0',
        'para' : '00',
        'upass' : pwd
    }).encode(encoding = 'UTF-8')
    request = urllib.request.Request(url = API_URL.format(operation = OPERATION_LOGIN, wlanuserip = get_wlan_user_ip(), wlancip = get_wlan_cip(), iTermType = ITERM_TYPE_PC), data = post_data)
    return urllib.request.urlopen(request).read().decode(encoding = 'GBK')

def logout():
    return urllib.request.urlopen(API_URL.format(operation = OPERATION_LOGOUT, wlanuserip = get_wlan_user_ip(), wlancip = get_wlan_cip(), iTermType = ITERM_TYPE_PC)).read().decode(encoding = 'GBK')

def checkerr():
    return urllib.request.urlopen(API_ERRCODE_URL).read().decode()

def get_wlan_user_ip():
    IPs = socket.gethostbyname_ex(socket.gethostname())[-1]
    for IP in IPs:
        try:
            if IP.index('172') == 0:
                return IP
        except ValueError:
            pass
    return ''

def get_wlan_cip():
    uip = get_wlan_user_ip()
    if len(uip) <= 0:
        return ''
    else:
        ip_addr = uip.split('.')
        return '{0}.{1}.255.250'.format(ip_addr[0], ip_addr[1])

def print_help():
    print('SCUT WiFi Login Helper 0.1 - For dormitory\n')
    print('Usage:')
    print('scutwifi_dormitory.py\tlogin username password\t : Login WiFi by username(Student ID) and password.')
    print('\t\t\tlogout\t\t\t : Log out WiFi')
    print('\t\t\tip\t\t\t : Get my wifi ip (Only SCUTWiFi)')
    print('\t\t\tcheckerr\t\t\t : Check error status')

def main():
    if len(sys.argv) < 2:
        print_help()
    else:
        if sys.argv[1] == 'login':
            if len(sys.argv) == 4:
                print(login(sys.argv[2], sys.argv[3]))
            else:
                print('Invaild arugments. Please check your command.')
        elif sys.argv[1] == 'logout':
            print(logout())
        elif sys.argv[1] == 'ip':
            print(get_wlan_user_ip())
        elif sys.argv[1] == 'checkerr':
            print(checkerr())
        else:
            print_help()

if __name__ == '__main__':
    main()
