# -*- coding:utf-8 -*


#nothing
import os
import requests
import time

from liepin_analyzer import liepin_anar

arr_404 = []
issue_array = []
err_counter = 0
success_counter = 0
invalid_counter = 0

def get_next_seed(seed):
    return seed + 1

def build_url(seed):
    template = "https://www.liepin.com/job/{0}.shtml"
    return template.format(seed)

def data_from_url(the_url):
    r = requests.get(the_url)
        
    ret_val = r.content.decode('utf-8').encode('gbk', 'ignore')
    if "error404_box" in ret_val:
        arr_404.append(the_url)
        return []
    else:
        return ret_val.split('\n')

    nfile = ""

    if "198017263" in the_url:
        nfile = "p1.txt"
    elif "198017264" in the_url:
        nfile = "p1.txt"
    elif "198017265" in the_url:
        nfile = "p3.txt"
        
    fd = open(nfile, 'r')
    lines = fd.readlines()
    fd.close()
    
    return lines

def do_work():
    users = []
    global err_counter
    global success_counter
    global invalid_counter
    
    seed = 198000001
    bar = seed + 1000

    while seed <= bar:
        req_url = build_url(seed)
        print "processing ", req_url

        try:
            lines = data_from_url(req_url)

            if len(lines) == 0:
                pass
            else:
                obj = liepin_anar(lines)
                obj.process()

                if obj.valid():
                    users.append(obj)
                    success_counter += 1
                else:
                    invalid_counter += 1
        except Exception, e:
            issue_array.append(req_url)
            print req_url, e
            
            err_counter += 1
        finally:            
            seed = get_next_seed(seed)
    return users

def print_something(users):
    for item in users:
        print item.job_title
        
def showERR():
    print "404 pages == ", len(issue_array)
    for item in issue_array:
        print "\t", item
    
def show404():
    print "404 pages == ", len(arr_404)
    for item in arr_404:
        print "\t", item
def test_request():
    '''
        1. pip install requests ---(reqeust != requests)
        2. import requests
        3. use it
    Problem:
        take care of encoding.
        --reference http://www.jb51.net/article/64816.htm
        encoding error in console.
        --decoding then encoding
        local variable 'err_counter' referenced before assignment
        ---global xxx in the function.
        
    '''
    seed = 198017263
    req_url = build_url(seed)
    r = requests.get(req_url)

    print r.content.decode('utf-8').encode('gbk', 'ignore')
    
    return
if __name__ == '__main__':
    arr_404 = []
    issue_array = []
    err_counter = 0
    success_counter = 0
    invalid_counter = 0
    
    starter = time.time()    
    users = do_work()
    ender = time.time()
    
    show404()
    total = err_counter + invalid_counter + success_counter + len(arr_404)
    print "404\t", len(arr_404)
    print "failed\t", err_counter
    print "invalid\t", invalid_counter
    print "success\t", success_counter
    print "total\t", total
    print ender, starter, ender - starter
    print "average = ", (ender - starter) / total
