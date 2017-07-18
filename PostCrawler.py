import traceback
import sys
import time
import random
import json
import getpass
sys.path.append('../PTTCrawlerLibrary')
import PTT
import os
print('Welcome to PostCrawler v 1.0.17.0718')

# 如果你想要自動登入，建立 Account.txt
# 然後裡面填上 {"ID":"YourID", "Password":"YourPW"}

try:
    with open('Account.txt', encoding = 'utf-8-sig') as AccountFile:
        Account = json.load(AccountFile)
        ID = Account['ID']
        Password = Account['Password']
    print('Auto ID password mode')
except FileNotFoundError:
    ID = input('輸入使用者帳號: ')
    Password = getpass.getpass('輸入密碼: ')
Board = sys.argv[1]

print(Board + ' Post Crawler')

if not os.path.exists(Board):
    os.makedirs(Board)

PTTCrawler = PTT.Crawler(ID, Password, True)

def PostCallBack(Post):
    
    try:
        os.makedirs(Post.getPostBoard() + '/' + Post.getPostID())
    except FileExistsError:
        pass
        
    f = open(Post.getPostBoard() + '/' + Post.getPostID() + '/Content.txt', 'w', encoding='utf-8-sig')
    f.write(Post.getTitle() + '\r\n')
    f.write(Post.getPostContent())
    f.close()
    
    f = open(Post.getPostBoard() + '/' + Post.getPostID() + '/PushList.txt', 'w', encoding='utf-8-sig')
    for Push in Post.getPushList():
        f.write(str(Push.getPushType()) + ' ' + Push.getPushContent() + '\r\n')
    f.close()
    
if not PTTCrawler.isLoginSuccess():
    PTTCrawler.Log('Login fail')
else:

    try:
    
        PTTCrawler.crawlBoard(Board, PostCallBack)

    except KeyboardInterrupt:
        '''
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
        '''
        PTTCrawler.Log('使用者中斷')
        PTTCrawler.logout()
        sys.exit()
    except EOFError:
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
    except ConnectionAbortedError:
        pass
    except Exception:
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)

