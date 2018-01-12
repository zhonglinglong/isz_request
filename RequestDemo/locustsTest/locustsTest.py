# -*- coding:utf8 -*-

import subprocess
from common.interface import get_cookie
from common.base import get_conf
from locust import HttpLocust, TaskSet
import webbrowser
import json


headers = {
    'content-type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
    #'User-Agent': 'spiderRN/2 CFNetwork/889.9 Darwin/17.2.0'
}
cookies = eval(get_conf('cookieInfo', 'cookies'))

def post(obj, url, data):
    with obj.client.post(url, data=data, headers=headers, cookies=cookies, catch_response=True) as response:
        if response.status_code != 200:
            print 'url：%s' % url, response.status_code
            print '响应状态码：%s' % response.status_code
            print u'响应信息：%s' % response.text
            response.failure(response.status_code)
        else:
            result = json.loads(response.text)
            if result['msg'] != 'ok':
                print response.text.encode('utf-8')
                response.failure(result)
            else:
                response.success()

def search_lock_list(obj):
    url = '/isz_thirdparty/smartLockSearchController/searchSmartLockHouseList.action'
    data = json.dumps({
        "pageNumber": 1, "pageSize": 50, "from": "lockHouseList"
    })
    post(obj, url, data)

def search_apartment_contract_list(obj):
    url = '/isz_contract/ApartmentContractController/searchApartmentContractListByEs.action'
    data = json.dumps({
        "sort": "create_time", "order": "desc", "pageNumber": 1, "pageSize": 50, "entrust_type": "SHARE",
        "notQueryCount": 'false', "total": 145, "current_dep_id": "00000000000000000000000000000000"
    })
    post(obj, url, data)

def search_customer_list(obj):
    url = '/isz_customer/CustomerController/searchEsCustomerList.action'
    data = json.dumps({
        "date_search_combo": "1", "pageNumber": 1, "pageSize": 50, "sort": "create_time", "order": "DESC",
        "current_dep_id": "00000000000000000000000000000000"
    })
    post(obj, url, data)

def search_apartment_list(obj):
    url = '/isz_house/ApartmentController/searchApartmentList.action'
    data = json.dumps({
        "other": "1", "pageNumber": "1", "pageSize": "50", "formType": "aparetment"
    })
    post(obj, url, data)


class WebsiteTasks(TaskSet):
    tasks = [search_apartment_list]
    def on_start(self):
        pass

class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = 'http://isz.ishangzu.com'
    # min_wait = 5000
    # max_wait = 10000

if __name__ == '__main__':
    get_cookie()
    debug = False
    if debug:
        sp = subprocess.Popen('locust -f .\locustsTest.py --no-web -c 1 -r 1', shell=True)
        sp.wait()
    else:
        test = subprocess.Popen('locust -f .\locustsTest.py')
        webbrowser.open('http://localhost:8089')
        test.wait()