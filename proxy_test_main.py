import logging
import time
from HTTP_Request_Randomizer.http_request_randomizer.requests.proxy.requestProxy import RequestProxy



if __name__ == '__main__':


    start = time.time()
    req_proxy = RequestProxy(log_level=logging.DEBUG)
    print("Initialization took: {0} sec".format((time.time() - start)))
    print("Size: {0}".format(len(req_proxy.get_proxy_list())))
    print("ALL = {0} ".format(list(map(lambda x: x.get_address(), req_proxy.get_proxy_list()))))

    test_url = 'http://ipv4.icanhazip.com'

    while True:
        start = time.time()
        request = req_proxy.generate_proxied_request(test_url)
        print("Proxied Request Took: {0} sec => Status: {1}".format((time.time() - start), request.__str__()))
        if request is not None:
            print("\t Response: ip={0}".format(u''.join(request.text).encode('utf-8')))
        print("Proxy List Size: {0}".format(len(req_proxy.get_proxy_list())))

        print("-> Going to sleep..")
        time.sleep(1)



    """
   
    proxyDic = {"free-proxy":"https://premproxy.com/list/"}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(proxyDic.get("free-proxy"), headers=headers, timeout=5)


    content = response.content
    #print(content)
    soup = BeautifulSoup(content, "html.parser")
    #print(proxyDic.get("free-proxy"))
    #print(soup)
    table = soup.find("table", attrs={"id": "proxylistt"})
    print(table)

    headings = [th.get_text() for th in table.find("tr").find_all("th")]
    datasets = []
    for row in table.find_all("tr")[1:-1]:
        dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
        if dataset:
            datasets.append(dataset)


    for dataset in datasets:
        #for data in dataset:
        #    print(data)
        proxy_obj = self.create_proxy_object(dataset)
        # Make sure it is a Valid Proxy Address
        if proxy_obj is not None and UrlParser.valid_ip_port(proxy_obj.get_address()):
            curr_proxy_list.append(proxy_obj)
        else:
            logger.debug("Proxy Invalid: {}".format(dataset))
        
    

    print(headings)
    print(datasets)
    """

