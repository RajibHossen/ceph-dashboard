import ceph_rest_api
import requests


app = ceph_rest_api.generate_app('/etc/ceph/ceph.conf','ceph','client.panel','panel','args')
#print app.ceph_addr
#print app.ceph_port

#http = requests.Session()
#headers = {'Content-type': 'application/json','Accept':'application/json'}
#url = 'http://' + str(app.ceph_addr) +':'+ str(app.ceph_port) + '/api/v0.1'
#print url
#try:
    #    r = requests.get(url,headers=headers)
    #except Exception as e:
        #    print e
