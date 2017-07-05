import traceback
import sys
import time
import random
import json
import getpass
sys.path.append('../PTTCrawlerLibrary')
import PTT
import os
print('Welcome to PostCrawler v 1.0.17.0703')

# If you want to automatically login define Account.txt
# {"ID":"YourID", "Password":"YourPW"}
try:
    with open('Account.txt', encoding = 'utf-8-sig') as AccountFile:
        Account = json.load(AccountFile)
        ID = Account['ID']
        Password = Account['Password']
    print('Auto ID password mode')
except FileNotFoundError:
    ID = input('Input ID: ')
    Password = getpass.getpass('Input password: ')
Board = sys.argv[1]

print(Board + ' Post Crawler')
StartIndex = int(input('Input start index: '))


Retry = True

if not os.path.exists(Board):
    os.makedirs(Board)

PTTCrawler = PTT.Crawler(ID, Password, False)

def SavePost(Board, Index):
    ErrorCode, Post = PTTCrawler.getPostInfoByIndex(Board, Index)
    if ErrorCode == PTTCrawler.PostDeleted:
        PTTCrawler.Log(str(Index) + ' has been deleted')
        return False
    if ErrorCode == PTTCrawler.WebFormatError:
        PTTCrawler.Log(str(Index) + ' Web structure error')
        return False
    if ErrorCode != PTTCrawler.Success:
        PTTCrawler.Log(str(Index) + ' getPostInfo ErrorCode: ' + str(ErrorCode))
        return False
    if Post == None:
        PTTCrawler.Log(str(Index) + ' getPostInfo unknow error')
        return False
    if not os.path.exists(Board + '/' + str(Index)):
        os.makedirs(Board + '/' + str(Index))
    
    f = open(Board + '/' + str(Index) + '/Author.txt', 'w')
    Author = Post.getPostAuthor()
    Author = Author[:Author.find(' (')]
    f.write(Author)
    f.close()
    
    f = open(Board + '/' + str(Index) + '/Content.txt', 'w')
    f.write(Post.getTitle())
    f.write(Post.getPostContent())
    f.close()
    
    f = open(Board + '/' + str(Index) + '/PushList.txt', 'w')
    for Push in Post.getPushList():
        f.write(str(Push.getPushType()) + ' ' + Push.getPushContent() + '\r')
    f.close()
    
    PTTCrawler.Log(Board + ' ' + str(Index) + ' save success')
    return True

if not PTTCrawler.isLoginSuccess():
    PTTCrawler.Log('Login fail')
else:
    #PTTCrawler.setLogLevel(PTTCrawler.LogLevel_DEBUG)
    try:
        while True:
            ErrorCode, LastIndexList = PTTCrawler.getNewPostIndexList(Board, StartIndex)
            if ErrorCode != PTTCrawler.Success:
                PTTCrawler.Log('getNewPostIndexList error')
                continue
            if len(LastIndexList) != 0:
                PTTCrawler.Log('Find new post')
                for index in LastIndexList:
                    SavePost(Board, index)
            time.sleep(10)
            
    except KeyboardInterrupt:
        '''
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
        '''
        PTTCrawler.Log('Interrupted by user')
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

