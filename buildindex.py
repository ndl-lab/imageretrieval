import numpy as np
import pickle
import time
import glob
import yaml
import json
from io import StringIO
import urllib.request, urllib.parse
import codecs
proxy_support = urllib.request.ProxyHandler({})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)

start = time.time()

#ids=[]
#uris=[]
#normvectors=[]
results=[]
idcnt=0
for fpath in glob.glob("ngtpkl/ngt.pkl"):
    f=open(fpath,"rb")
    datalist=pickle.load(f)
    renban=set()
    renbancnt=0
    for dic in datalist:
        vector=dic["vec"]
        pid=str(dic["iiif"]).split("/")[0]
        koma=str(int(str(dic["iiif"]).split("/")[1][1:]))
        idn=pid+"_"+koma+"_"+str(renbancnt)
        while idn in renban:
            renbancnt+=1
            idn=pid+"_"+koma+"_"+str(renbancnt)
        renban.add(idn)
        renbancnt=0
        #print(idn)
        normalized_vector = vector / np.linalg.norm(vector)
        normalized_vector = normalized_vector.tolist()
        try:
            url = 'http://localhost:10000/insert'
            #req = urllib.request.Request(url)
            query={'id':idn,'vector':normalized_vector}
            #print(query)
            headers = {'Content-Type': 'application/json'}
            req = urllib.request.Request(url, json.dumps(query).encode(), headers)
            try:
                with urllib.request.urlopen(req,timeout=10) as res:
                    responseBody = res.read()
            except urllib.error.HTTPError as err:
                    print(err.code)
                    print(err)
            except urllib.error.URLError as err:
                    print(err.reason)
        except Exception as e:
            print("An error occured")
            print("The information of error is as following")
            print(type(e))
            print(e.args)
            print(e)
        idcnt+=1
    f.close()
urlcreate = 'http://localhost:10000/index/create/8'
urlsave = 'http://localhost:10000/index/save'
#del index
try:
    with urllib.request.urlopen(urlcreate,timeout=10000) as res:
        responseBody = res.read()
except urllib.error.HTTPError as err:
    print(err.code)
    print(err)
except urllib.error.URLError as err:
    print(err.reason)
try:
    with urllib.request.urlopen(urlsave,timeout=10000) as res:
        responseBody = res.read()
except urllib.error.HTTPError as err:
    print(err.code)
    print(err)
except urllib.error.URLError as err:
    print(err.reason)
