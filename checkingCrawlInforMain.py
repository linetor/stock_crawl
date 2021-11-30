from CrawlCompanyInfor import CrawlCompanyInfor




if __name__ == '__main__':
    crawlCompanyInfor = CrawlCompanyInfor()
    print(crawlCompanyInfor.insertCompanyInfor())
    del crawlCompanyInfor
    print("end")
    #print(CrawlCompanyInfor.getStockByCode())
