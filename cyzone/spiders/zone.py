# -*- coding: utf-8 -*-
import scrapy

try:
    from cyzone.cyzone.items import CompanyItem, VocationItem, \
        TurnItem, TeamItem, ExampleItem, PeopleItem, VcompanyItem
except:
    from ..items import CompanyItem, VocationItem, \
        TurnItem, TeamItem, ExampleItem, PeopleItem, VcompanyItem
DEBUG = True  # True表示不会获取下一页的数据 只会获取第一页


class ZoneSpider(scrapy.Spider):
    name = 'zone'
    allowed_domains = ['www.cyzone.cn']
    start_urls = ['http://www.cyzone.cn/']

    def start_requests(self):
        # 知名投资人列表
        people_url = "http://www.cyzone.cn/people/list-0-1-0-0/"
        yield scrapy.Request(people_url, callback=self.parse_people_list)
        # 创业公司列表
        vcom_url = "http://www.cyzone.cn/vcompany/list-0-0-1-0-0/"
        yield scrapy.Request(vcom_url, callback=self.parse_v_company)
        # 投资机构列表
        base_url = "http://www.cyzone.cn/company/list-0-1-4/"
        yield scrapy.Request(base_url, callback=self.parse_list)

    # 处理知名投资人列表
    def parse_people_list(self, response):
        peopleList = response.xpath('//tr[@class="ltp-plate"]')
        for people in peopleList:
            username = "".join(people.xpath('td[2]/a/text()').extract())  # 个人名字
            image = "".join(people.xpath('td[1]/div[1]/a/img/@src').extract())  # 人物图片
            company = "".join(people.xpath('td[3]/a/text()').extract())  # 投资机构
            detail_url = "".join(people.xpath('td[1]/div[1]/a/@href').extract())  # 详情页链接
            yield scrapy.Request(detail_url,
                                 callback=self.parse_people_detail,
                                 meta={"username": username,
                                       "image": image,
                                       "company": company,
                                       "detail_url": detail_url,
                                       })
        next_page = "".join(
            response.xpath('//*[@id="pages"]/span[@class="current"]/following-sibling::*[1]/@href').extract())
        if next_page:
            url = response.urljoin(next_page)
            if not DEBUG:
                yield scrapy.Request(url, callback=self.parse_people_list)

    # 处理知名投资人详情页信息
    def parse_people_detail(self, response):
        people_item = PeopleItem()
        people_item["username"] = response.meta["username"]  # 个人名字
        people_item["image"] = response.meta["image"]  # 人物图片
        people_item["company"] = response.meta["company"]  # 投资机构
        people_item["detail_url"] = response.meta["detail_url"]
        people_item["job"] = "|".join(
            response.xpath('//div[@class="top-info clearfix top-info-vpeople"]/div[1]/ul/li/text()').extract())  # 职业、头衔
        people_item["field"] = "|".join(response.xpath('//div[@class="invest"]/div[1]/span/text()')
                                        .extract())[6:]  # 关注投资领域
        people_item["period"] = "|".join(response.xpath('//div[@class="invest"]/div[2]/span/text()')
                                         .extract())[6:]  # 投资阶段
        if "|".join(response.xpath('//div[@class="invest"]/div[3]/span[1]/text()').extract()) == "常驻城市：":
            people_item["invest"] = ""
            people_item["city"] = "|".join(response.xpath('//div[@class="invest"]/div[3]/span/text()')
                                           .extract())[6:]  # 常驻城市
        elif "|".join(response.xpath('//div[@class="invest"]/div[3]/span[1]/text()').extract()) == "单笔投资：":
            people_item["invest"] = "|".join(response.xpath('//div[@class="invest"]/div[3]/span/text()')
                                             .extract())[6:]  # 单笔投资金额
            people_item["city"] = "|".join(response.xpath('//div[@class="invest"]/div[4]/span/text()')
                                           .extract())[6:]  # 常驻城市
        else:
            people_item["invest"] = ""
            people_item["city"] = ""
        people_item["information"] = "".join(response.xpath('//div[@class="people-info"]/div[1]/div/p/text()|\
                                                   //div[@class="people-info"]/div[1]/div/p/a/text()').extract())  # 简介
        experienceList = response.xpath('//div[@class="record"]/div')
        experienceS = []
        for exper in experienceList:
            s = "/".join(exper.xpath('div/div/div/span/a/text()|div/div/div/span/text()|div/div/div/text()').extract())
            experienceS.append(s.replace('//', ''))
        people_item["experience"] = " | ".join(experienceS).replace('\n', '').replace('\t', '').replace('\r', '')  # 经历
        yield people_item

    # 处理所有的创业公司列表
    def parse_v_company(self, response):
        v_company_list = response.xpath('//div[@class="list-table"]/table/tr')
        for v_company in v_company_list[1:]:
            image = "".join(v_company.xpath('td[1]/a/img/@src').extract())
            name = "".join(v_company.xpath('td[2]/a/span/text()').extract())
            period = "".join(v_company.xpath('td[3]/a/text()').extract())
            field = "".join(v_company.xpath('td[4]/a/text()').extract())
            become_time = "".join(v_company.xpath('td[5]/text()').extract())
            detail_url = "".join(v_company.xpath('td[2]/a/@href').extract())
            yield scrapy.Request(detail_url,
                                 callback=self.parse_v_company_detail,
                                 meta={
                                     "image": image,
                                     "name": name,
                                     "period": period,
                                     "field": field,
                                     "become_time": become_time,
                                     "detail_url": detail_url,
                                 })
        next_page = "".join(
            response.xpath('//*[@id="pages"]/span[@class="current"]/following-sibling::*[1]/@href').extract())
        if next_page:
            url = response.urljoin(next_page)
            if not DEBUG:
                yield scrapy.Request(url, callback=self.parse_v_company)

    # 处理创业公司详情页信息
    def parse_v_company_detail(self, response):
        item_v_company = VcompanyItem()
        item_v_company["image"] = response.meta["image"]
        item_v_company["name"] = response.meta["name"]
        item_v_company["period"] = response.meta["period"]
        item_v_company["field"] = response.meta["field"]
        item_v_company["become_time"] = response.meta["become_time"]
        item_v_company["detail_url"] = response.meta["detail_url"]
        item_v_company["all_name"] = "".join(
            response.xpath('//div[@class="top-info clearfix"]/div[1]/ul/li[@class="time"]/text()').extract())[
                                     5:]  # 公司全称
        item_v_company["web"] = "".join(response.xpath(
            '//div[@class="top-info clearfix"]/div[1]/ul/li[@class="add clearfix"]/a/text()|\
            //div[@class="com-url"]/a/text()').extract())  # 公司官网
        item_v_company["place"] = "".join(response.xpath(
            '//div[@class="all-info"]/div[1]/div[2]/div[1]/div[2]/ul/li[2]/span/a/text()').extract())  # 公司位置
        item_v_company["content"] = "/".join(response.xpath(
            '//div[@class="all-info"]/div[1]/div[2]/div[1]/div[2]/ul/li[4]/span/a/text()').extract())  # 主要服务内容
        item_v_company["introduction"] = "".join(
            response.xpath('//div[@class="all-info"]/div[1]/div[2]/div[1]/div[3]/div/p/text()').extract())  # 简介
        dynamicList = response.xpath('//div[@class="trends clearfix look"]/div/div')
        dynamic_s = []
        for dynamic in dynamicList:
            times = "".join(dynamic.xpath('div[2]/span/text()').extract())  # 动态发生时间
            info = "".join(dynamic.xpath('div[3]/div/text()|div[3]/div/a/text()|\
                                        div[3]/div/p/text()|\
                                        div[3]/div/p/span/text()').extract()) \
                .replace('\n', '').replace('\t', '').replace('\r', '')  # 动态内容
            dynamic_s.append("时间：{} / 事件：{}".format(times, info))
        item_v_company["dynamic"] = " | ".join(dynamic_s)  # 公司动态
        money_experience_s = []
        money_experienceList = response.xpath('div[@class="live"]/table/tbody/tr')
        for money in money_experienceList[1:]:
            money_period = "".join(money.xpath('td[1]/text()').extract())
            money_num = "".join(money.xpath('td[2]/div[2]/text()').extract())
            money_company = "".join(money.xpath('td[3]/a/text()').extract())
            money_day = "".join(money.xpath('td[4]/text()').extract())
            money_experience_s.append("阶段：{}/融资金额：{}/投资方：{}/融资日期：{}"
                                      .format(money_period, money_num, money_company, money_day))
        item_v_company["money_experience"] = " | ".join(money_experience_s)  # 融资经历
        # 工商信息
        item_v_company["register_num"] = "".join(response.xpath('//*[@id="qcc"]/div/p[1]/text()').extract())  # 注册号
        item_v_company["run_status"] = "".join(response.xpath('//*[@id="qcc"]/div/p[2]/text()').extract())  # 经营状态
        item_v_company["law_represent"] = "".join(response.xpath('//*[@id="qcc"]/div/p[3]/text()').extract())  # 法人代表
        item_v_company["shareholder"] = "|".join(response.xpath('//*[@id="qcc"]/div/p[4]/span[2]/text()').extract()) \
            .replace('\n', '').replace('\t', '').replace('\r', '')  # 股东
        item_v_company["company_type"] = "".join(response.xpath('//*[@id="qcc"]/div/p[5]/text()').extract())  # 公司类型
        item_v_company["com_day"] = "".join(response.xpath('//*[@id="qcc"]/div/p[6]/text()').extract())  # 公司注册成立日期
        item_v_company["register_money"] = "".join(response.xpath('//*[@id="qcc"]/div/p[7]/text()').extract())  # 注册资金
        item_v_company["detail_place"] = "".join(response.xpath('//*[@id="qcc"]/div/p[8]/text()').extract())  # 公司住所
        yield item_v_company

    # 处理投资机构列表
    def parse_list(self, response):
        company_list = response.xpath('//div[@class="list-table2"]/table/tr')
        for company in company_list[1:]:
            image = "".join(company.xpath('td[1]/a/img/@src').extract())
            # web = "".join(company.xpath('td[1]/a/img/@src').extract())# 官网
            name = "".join(company.xpath('td[2]/a/span/text()').extract())
            become_time = "".join(company.xpath('td[3]/text()').extract())
            investment_case = "".join(company.xpath('td[4]/text()').extract())
            like = "".join(company.xpath('td[5]/text()').extract())
            field = "".join(company.xpath('td[6]/text()').extract())
            detail_url = "".join(company.xpath('td[2]/a/@href').extract())
            yield scrapy.Request(detail_url,
                                 callback=self.parse_company_detail,
                                 meta={
                                     "image": image,
                                     "name": name,
                                     "become_time": become_time,
                                     "investment_case": investment_case,
                                     "like": like,
                                     "field": field,
                                     "detail_url": detail_url,
                                 })
        next_page = "".join(
            response.xpath('//*[@id="pages"]/span[@class="current"]/following-sibling::*[1]/@href').extract())
        if next_page:
            url = response.urljoin(next_page)
            if not DEBUG:
                yield scrapy.Request(url, callback=self.parse_list)

    # 投资机构的详情页
    def parse_company_detail(self, response):
        company_item = CompanyItem()
        company_item["detail_url"] = response.meta["detail_url"]
        company_item["image"] = response.meta["image"]
        # web = "".join(company.xpath('td[1]/a/img/@src').extract())# 官网
        company_item["name"] = response.meta["name"]
        company_item["become_time"] = response.meta["become_time"]
        company_item["investment_case"] = response.meta["investment_case"]
        company_item["like"] = response.meta["like"]
        company_item["field"] = response.meta["field"]
        company_item["information"] = "".join(response.xpath('//div[@class="people-info-box"]/p//text()').extract())
        company_item["web"] = "".join(response.xpath('//a[@class="web"]/@href').extract())
        company_item["icon1_num"] = "".join(response.xpath('//div[@class="num num1"]/text()').extract())
        company_item["icon2_num"] = "".join(response.xpath('//div[@class="num num2"]/text()').extract())
        company_item["icon3_num"] = "".join(response.xpath('//div[@class="num num3"]/text()').extract())
        yield company_item
        #  投资机构的团队成员
        team_list = response.xpath('//div[@class="team clearfix look"]/ul/li')
        for team in team_list:
            name = company_item["name"]
            image = "".join(team.xpath('div[1]/a/img/@src').extract())  # 个人图片
            username = "".join(team.xpath('div[2]/p[1]/a/text()').extract())  # 个人名字
            detail_url = "".join(team.xpath('div[2]/p[1]/a/@href').extract())  # 详情页地址
            yield scrapy.Request(detail_url,
                                 callback=self.parse_team_people,
                                 meta={
                                     "name": name,
                                     "image": image,
                                     "username": username,
                                     "detail_url": detail_url,
                                 })
        # # 投资行业数据=============
        # # com_1 = re.compile(r'data: (\[.*?\])')
        # # 投资机构投资轮次数据
        # # 正则匹配
        #
        # # 投资案例
        case_url = "".join(response.xpath('//div[@class="check-more2"]/a/@href').extract())
        if case_url:
            yield scrapy.Request(case_url,
                                 callback=self.parse_case,
                                 meta={"name": company_item["name"]})
        else:
            # 直接解析当前页面所有的案例
            case_list = response.xpath('//div[@class="live"]/table/tr')
            for case in case_list[1:]:
                example_item = ExampleItem()
                example_item["name"] = company_item["name"]  # 投资机构名称
                example_item["web"] = "".join(case.xpath('td[1]/a/@href').extract())
                example_item["company"] = "".join(case.xpath('td[1]/a/text()').extract())  # 投资公司
                example_item["money"] = "".join(case.xpath('td[2]/div[@class="money"]/text()').extract())  # 投资金额
                example_item["turn"] = "".join(case.xpath('td[4]/text()').extract())  # 轮次
                example_item["vocation"] = "".join(case.xpath('td[3]/text()').extract())  # 行业
                example_item["times"] = "".join(case.xpath('td[5]/text()').extract())  # 投资时间
                example_item["image"] = ""  # 公司图片
                # industry_average = "".join(case.xpath('td[1]/a/@href').extract())  # 行业平均数据
                yield example_item

    # 处理投资机构的团队人员信息
    def parse_team_people(self, response):
        team_item = TeamItem()
        team_item["name"] = response.meta["name"]
        team_item["image"] = response.meta["image"]
        team_item["username"] = response.meta["username"]
        team_item["detail_url"] = response.meta["detail_url"]
        team_item["job"] = "".join(
            response.xpath('//div[@class="top-info clearfix top-info-vpeople"]/div[1]/ul/li/text()').extract())  # 职业、头衔
        team_item["fild"] = "".join(response.xpath('//div[@class="invest"]/div[1]/span/text()').extract())  # 关注投资领域
        team_item["period"] = "".join(response.xpath('//div[@class="invest"]/div[2]/span/text()').extract())  # 投资阶段
        if "|".join(response.xpath('//div[@class="invest"]/div[3]/span[1]/text()').extract()) == "常驻城市：":
            team_item["invest"] = ""
            team_item["city"] = "|".join(response.xpath('//div[@class="invest"]/div[3]/span/text()')
                                         .extract())[6:]  # 常驻城市
        elif "|".join(response.xpath('//div[@class="invest"]/div[3]/span[1]/text()').extract()) == "单笔投资：":
            team_item["invest"] = "|".join(response.xpath('//div[@class="invest"]/div[3]/span/text()')
                                           .extract())[6:]  # 单笔投资金额
            team_item["city"] = "|".join(response.xpath('//div[@class="invest"]/div[4]/span/text()')
                                         .extract())[6:]  # 常驻城市
        else:
            team_item["invest"] = ""
            team_item["city"] = ""
        team_item["information"] = "".join(response.xpath('//div[@class="people-info"]/div[1]/div/p/text()|\
                                            //div[@class="people-info"]/div[1]/div/p/a/text()').extract())  # 简介
        experienceList = response.xpath('//div[@class="record"]/div')
        experienceS = []
        for exper in experienceList:
            s = "/".join(exper.xpath('div/div/div/span/a/text()|div/div/div/span/text()|div/div/div/text()')
                         .extract())
            experienceS.append(s.replace('//', ''))
        team_item["experience"] = " | ".join(experienceS).replace('\n', '').replace('\t', '').replace('\r', '')  # 经历
        yield team_item

    # 处理投资机构案例
    def parse_case(self, response):
        name = response.meta["name"]
        case_list = response.xpath('//div[@class="list-table3"]/table/tr')
        for case in case_list[1:]:
            example_item = ExampleItem()
            example_item["name"] = name
            example_item["company"] = "".join(case.xpath('td[2]/span[2]/text()').extract())
            example_item["web"] = "".join(case.xpath('td[1]/a/@href').extract())
            example_item["image"] = "".join(case.xpath('td[1]/a/img/@src').extract())
            # industry_average = "".join(case.xpath('td[1]/a/img/@src').extract())
            example_item["money"] = "".join(case.xpath('td[3]/div[@class="money"]/text()').extract())
            example_item["turn"] = "".join(case.xpath('td[4]/text()').extract())
            example_item["vocation"] = "".join(case.xpath('td[6]/a/text()').extract())
            example_item["times"] = "".join(case.xpath('td[7]/text()').extract())
            yield example_item
        next_page = "".join(
            response.xpath('//*[@id="pages"]/span[@class="current"]/following-sibling::*[1]/@href').extract())
        if next_page:
            url = response.urljoin(next_page)
            if not DEBUG:
                yield scrapy.Request(url,
                                     callback=self.parse_case,
                                     meta={"name": name})
