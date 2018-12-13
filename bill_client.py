#!./python/bin/python
# -*- coding: utf-8 -*-
import time
import os
import sys
import requests
import json
import datetime

user_id = '2000001673' 
deadline = datetime.datetime.combine(datetime.date.today(), datetime.time.max) + datetime.timedelta(days=15)


def request_parse(resp):
    if resp.text:
        if resp.status_code == 400:
            if ('Connection refused' in resp.text or
                    'actively refused' in resp.text):
                raise Exception(resp.text)
        try:
            body = json.loads(resp.text)
        except ValueError:
            body = resp.text
    else:
        body = None

    if resp.status_code >= 400:
        msg = ("Request failed with status %s due to %s" % (resp.status_code, resp.text))
        print
        raise Exception(msg)

    return resp, body



def get_request_head():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'python-novaclient',
        }

    return headers


def do_creat_bill(bill_info):

    print("make a bill.")
   
    cpu = bill_info['cpu'] 
    mem = bill_info['mem']
    ssd = bill_info['ssd']
    
 
    body = {
    "userId": user_id,  #用户id
    "orderUse":4,       #购买定值
    "isBu":1,           #定值
    "orderType":3,      #定值
    "source":2,         #定值
    "sourceExtend":{    #定值
        "appId":"100.opcenter"
    },
    "products":[
        {   
            "num":1,    #个数
            "billType":5,   #计费方式
            "productType":41,   #主机类型IO
            "productUse":1, #定值
            "productWhat":2,    #定值
            "region":"T",#机
            "userId": user_id,  #用户Id
            "pEndTime": deadline.strftime("%Y-%m-%d %H:%M:%S"),        #到期时间
            "price": 0,
    
            ]
        }
    ]
    }
    url = "http://{{url}}/trade/saveOrder" 
    headers = get_request_head()
    #headers['body'] = body
    data = json.dumps(body)
    return request_parse(requests.post(url, headers=get_request_head(), data=data))
    


def create_bill(instance_uuid, bill_info):
    

    resp, body = do_creat_bill(bill_info)
    subOrderId = body['subOrderIds'][0] 
    if subOrderId is None:
        raise
    notify_bill(subOrderId, instance_uuid)
 

def notify_bill(subOrderId, instance_id):
    
    body = {
        "subOrderId": subOrderId,    #上个请求的子订单号
        "status": 1,                                 #1、成功，2、失败
        "instanceId": instance_id,    #主机的实例id
        "source":2                              #定值
    }
    url = "http://{url}/trade/notifySubOrderStatus" 
    headers = get_request_head() 
    data = json.dumps(body)
    resp, body = request_parse(requests.post(url, headers=get_request_head(), data=data))
    print '*' * 50
    print "Created bill."


 
    
 
if __name__ == "__main__":

    instance_uuid = '60329f69-136ebedded8561'
    bill_info = {}
    bill_info['cpu'] = 1
    bill_info['mem'] = 1
    bill_info['ssd'] = 50


    create_bill(instance_uuid, bill_info)
