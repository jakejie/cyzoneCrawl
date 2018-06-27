# -*- coding: utf-8 -*-
from datetime import datetime

try:
    from cyzone.cyzone.items import CompanyItem, VocationItem, \
        TurnItem, TeamItem, ExampleItem, PeopleItem, VcompanyItem, \
        Company, Vocation, Turn, Team, Example, People, Vcompany, \
        create_engine, db_user, db_pawd, db_host, db_port, db_name, sessionmaker
except:
    from .items import CompanyItem, VocationItem, \
        TurnItem, TeamItem, ExampleItem, PeopleItem, VcompanyItem, \
        Company, Vocation, Turn, Team, Example, People, Vcompany, \
        create_engine, db_user, db_pawd, db_host, db_port, db_name, sessionmaker


class CyzonePipeline(object):
    def __init__(self):
        engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'
                               .format(db_user, db_pawd, db_host, db_port, db_name), max_overflow=5000,
                               pool_recycle=3600, pool_size=5000)
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def process_item(self, item, spider):
        if isinstance(item, CompanyItem):
            print("投资机构")
            info = Company(
                detail_url=item["detail_url"],  # 机构详情页
                image=item["image"],  # 公司图片
                web=item["web"],  # 机构官网
                name=item["name"],  # 机构名称
                become_time=item["become_time"],  # 成立时间
                investment_case=item["investment_case"],  # 投资案例
                like=item["like"],  # 投资偏好
                field=item["field"],  # 专注投资领域
                information=item["information"],  # 机构简介
                icon1_num=item["icon1_num"],  # 披露的投资事件数
                icon2_num=item["icon2_num"],  # 走到下一轮公司数
                icon3_num=item["icon3_num"],  # 连续投资公司数
                # add_time = datetime.now(),
            )
        elif isinstance(item, TeamItem):
            print("投资机构团队成员")
            info = Team(
                name=item["name"],  # 外键关联投资机构
                image=item["image"],  # 个人图片
                detail_url=item["detail_url"],  # 详情页地址
                username=item["username"],  # 个人名字
                job=item["job"],  # 职业、头衔
                fild=item["fild"],  # 关注投资领域
                period=item["period"],  # 投资阶段
                invest=item["invest"],  # 单笔投资金额
                city=item["city"],  # 常驻城市
                information=item["information"],  # 简介
                experience=item["experience"],  # 经历
                add_time=datetime.now(),  # 数据添加时间
            )
        elif isinstance(item, ExampleItem):
            print("投资案例")
            info = Example(
                name=item["name"],
                company=item["company"],  # 投资公司
                web=item["web"],  # 投资公司
                money=item["money"],  # 投资金额
                image=item["image"],  # 投资金额
                turn=item["turn"],  # 轮次
                vocation=item["vocation"],  # 行业
                times=item["times"],  # 投资时间
                add_time=datetime.now(),  # 数据添加时间
            )
        elif isinstance(item, PeopleItem):
            print("知名投资人")
            info = People(
                detail_url=item["detail_url"],  # 详情页地址
                username=item["username"],  # 个人名字
                image=item["image"],  # 人物图片
                company=item["company"],  # 投资机构
                job=item["job"],  # 职业、头衔
                field=item["field"],  # 关注投资领域
                period=item["period"],  # 投资阶段
                invest=item["invest"],  # 单笔投资金额
                city=item["city"],  # 常驻城市
                information=item["information"],  # 简介
                experience=item["experience"],  # 经历
                add_time=datetime.now(),  # 数据添加时间
            )
        elif isinstance(item, VcompanyItem):
            print("创业公司")
            info = Vcompany(
                detail_url=item["detail_url"],
                image=item["image"],  # 公司图片
                name=item["name"],  # 公司名称
                all_name=item["all_name"],  # 公司全称
                period=item["period"],  # 融资阶段
                field=item["field"],  # 创业领域
                become_time=item["become_time"],  # 成立时间
                web=item["web"],  # 公司官网
                place=item["place"],  # 公司位置
                content=item["content"],  # 主要服务内容
                introduction=item["introduction"],  # 简介
                dynamic=item["dynamic"],  # 公司动态
                money_experience=item["money_experience"],  # 融资经历
                # 工商信息
                register_num=item["register_num"],  # 注册号
                run_status=item["run_status"],  # 经营状态
                law_represent=item["law_represent"],  # 法人代表
                shareholder=item["shareholder"],  # 股东
                company_type=item["company_type"],  # 公司类型
                com_day=item["com_day"],  # 公司注册成立日期
                register_money=item["register_money"],  # 注册资金
                detail_place=item["detail_place"],  # 公司住所
                add_time=datetime.now(),  # 数据添加时间
            )
        else:
            print("没有该分类:{}".format(item))
            info = False
            return item
        num = 0
        if info:
            while True:
                num = num + 1
                try:
                    self.session.add(info)
                    self.session.commit()
                    print("插入成功".center(20, "*"))
                    return item
                except Exception as e:
                    print("[UUU] Error :{}".format(e))
                    self.session.rollback()
