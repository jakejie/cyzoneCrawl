# -*- coding: utf-8 -*-
import time
from sqlalchemy import Column, String, create_engine, Integer, Text, ForeignKey
# from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import scrapy

# 创建对象的基类
Base = declarative_base()

# 数据库连接信息
db_host = '127.0.0.1'
db_user = 'root'
db_pawd = 'root'
db_name = 'cyzone'
db_port = 3306


# 所有的投资机构
class CompanyItem(scrapy.Item):
    detail_url = scrapy.Field()  # 机构详情页
    image = scrapy.Field()  # 公司图片
    web = scrapy.Field()  # 机构官网
    name = scrapy.Field()  # 机构名称
    become_time = scrapy.Field()  # 成立时间
    investment_case = scrapy.Field()  # 投资案例
    like = scrapy.Field()  # 投资偏好
    field = scrapy.Field()  # 专注投资领域
    information = scrapy.Field()  # 机构简介
    icon1_num = scrapy.Field()  # 披露的投资事件数
    icon2_num = scrapy.Field()  # 走到下一轮公司数
    icon3_num = scrapy.Field()  # 连续投资公司数
    add_time = scrapy.Field()  # 数据添加时间
    # turn = scrapy.Field()  # 投资轮次分布==正则 在html里提取
    # vocation = scrapy.Field()  # 投资行业分布==正则 在html里提取
    # team = scrapy.Field()  # 投资机构的团队人员
    # example = scrapy.Field()  # 机构投资案例


# 投资机构投资行业数据
class VocationItem(scrapy.Item):
    name = scrapy.Field()
    energy = scrapy.Field()  # 清洁技术/新能源
    cloud = scrapy.Field()  # 云服务
    bigdata = scrapy.Field()  # 大数据
    Inte_made = scrapy.Field()  # 智能制造
    web_finance = scrapy.Field()  # 互联网金融
    new_farming = scrapy.Field()  # 新农业
    logistics = scrapy.Field()  # 物流
    media_info = scrapy.Field()  # 媒体资讯
    O2O = scrapy.Field()  # O2O
    Inter_of_thing = scrapy.Field()  # 物联网
    ar_vr = scrapy.Field()  # ARVR
    share_enconomy = scrapy.Field()  # 共享经济
    others = scrapy.Field()  # 其他
    ai = scrapy.Field()  # 人工智能
    sty_enter = scrapy.Field()  # 文体娱乐
    market_adver = scrapy.Field()  # 营销广告
    outdoors = scrapy.Field()  # 旅游户外
    realty = scrapy.Field()  # 房产
    medical_health = scrapy.Field()  # 医疗健康
    traffic = scrapy.Field()  # 交通出行
    mobile_inter = scrapy.Field()  # 移动互联网
    tools = scrapy.Field()  # 工具软件
    social_real = scrapy.Field()  # 社交
    edu = scrapy.Field()  # 教育
    hardware = scrapy.Field()  # 硬件
    game_music = scrapy.Field()  # 游戏动漫
    living_consu = scrapy.Field()  # 生活消费
    financial_pay = scrapy.Field()  # 金融支付
    content_industry = scrapy.Field()  # 内容产业
    enterprice_service = scrapy.Field()  # 企业服务
    elect_business = scrapy.Field()  # 电子商务
    add_time = scrapy.Field()  # 数据添加时间


# 投资机构投资轮次数据
class TurnItem(scrapy.Item):
    name = scrapy.Field()
    Num_1 = scrapy.Field()  # 天使轮
    Num_A = scrapy.Field()  # 泛A轮
    Num_B = scrapy.Field()  # 泛B轮
    Num_C = scrapy.Field()  # 泛C轮
    Num_D = scrapy.Field()  # D轮至Pre-IPO
    Num_Z = scrapy.Field()  # 战略投资
    Num_O = scrapy.Field()  # 未透露
    add_time = scrapy.Field()  # 数据添加时间


# 投资机构的团队成员
class TeamItem(scrapy.Item):
    name = scrapy.Field()  # 外键关联投资机构
    image = scrapy.Field()  # 个人图片
    detail_url = scrapy.Field()  # 详情页地址
    username = scrapy.Field()  # 个人名字
    job = scrapy.Field()  # 职业、头衔
    fild = scrapy.Field()  # 关注投资领域
    period = scrapy.Field()  # 投资阶段
    invest = scrapy.Field()  # 单笔投资金额
    city = scrapy.Field()  # 常驻城市
    information = scrapy.Field()  # 简介
    experience = scrapy.Field()  # 经历
    add_time = scrapy.Field()  # 数据添加时间


# 机构投资案例
class ExampleItem(scrapy.Item):
    name = scrapy.Field()
    company = scrapy.Field()  # 投资公司
    image = scrapy.Field()  # 投资公司
    web = scrapy.Field()  # 投资公司
    money = scrapy.Field()  # 投资金额
    turn = scrapy.Field()  # 轮次
    vocation = scrapy.Field()  # 行业
    times = scrapy.Field()  # 投资时间
    add_time = scrapy.Field()  # 数据添加时间


# 知名投资人
class PeopleItem(scrapy.Item):
    detail_url = scrapy.Field()  # 详情页地址
    username = scrapy.Field()  # 个人名字
    image = scrapy.Field()  # 人物图片
    company = scrapy.Field()  # 投资机构
    job = scrapy.Field()  # 职业、头衔
    field = scrapy.Field()  # 关注投资领域
    period = scrapy.Field()  # 投资阶段
    invest = scrapy.Field()  # 单笔投资金额
    city = scrapy.Field()  # 常驻城市
    information = scrapy.Field()  # 简介
    experience = scrapy.Field()  # 经历
    add_time = scrapy.Field()  # 数据添加时间


# 创业公司
class VcompanyItem(scrapy.Item):
    detail_url = scrapy.Field()
    image = scrapy.Field()  # 公司图片
    name = scrapy.Field()  # 公司名称
    all_name = scrapy.Field()  # 公司全称
    period = scrapy.Field()  # 融资阶段
    field = scrapy.Field()  # 创业领域
    become_time = scrapy.Field()  # 成立时间

    web = scrapy.Field()  # 公司官网
    place = scrapy.Field()  # 公司位置
    content = scrapy.Field()  # 主要服务内容
    introduction = scrapy.Field()  # 简介
    dynamic = scrapy.Field()  # 公司动态
    money_experience = scrapy.Field()  # 融资经历
    # 工商信息
    register_num = scrapy.Field()  # 注册号
    run_status = scrapy.Field()  # 经营状态
    law_represent = scrapy.Field()  # 法人代表
    shareholder = scrapy.Field()  # 股东
    company_type = scrapy.Field()  # 公司类型
    com_day = scrapy.Field()  # 公司注册成立日期
    register_money = scrapy.Field()  # 注册资金
    detail_place = scrapy.Field()  # 公司住所
    add_time = scrapy.Field()  # 数据添加时间


# 所有的投资机构
class Company(Base):
    # 表名
    __tablename__ = 'company'
    id = Column(Integer, unique=True, primary_key=True)
    detail_url = Column(String(64))  # 机构详情页
    image = Column(String(256))  # 公司图片
    web = Column(String(512))  # 机构官网
    name = Column(String(512))  # 机构名称
    become_time = Column(String(16))  # 成立时间
    investment_case = Column(String(8))  # 投资案例
    like = Column(String(512))  # 投资偏好
    field = Column(String(512))  # 专注投资领域
    information = Column(Text)  # 机构简介
    icon1_num = Column(String(8))  # 披露的投资事件数
    icon2_num = Column(String(8))  # 走到下一轮公司数
    icon3_num = Column(String(8))  # 连续投资公司数
    add_time = Column(String(32))  # 数据添加时间


# 投资机构投资行业数据
class Vocation(Base):
    __tablename__ = "vocation"
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(512))  # 投资机构名称
    energy = Column(Integer)  # 清洁技术/新能源
    cloud = Column(Integer)  # 云服务
    bigdata = Column(Integer)  # 大数据
    Inte_made = Column(Integer)  # 智能制造
    web_finance = Column(Integer)  # 互联网金融
    new_farming = Column(Integer)  # 新农业
    logistics = Column(Integer)  # 物流
    media_info = Column(Integer)  # 媒体资讯
    O2O = Column(Integer)  # O2O
    Inter_of_thing = Column(Integer)  # 物联网
    ar_vr = Column(Integer)  # ARVR
    share_enconomy = Column(Integer)  # 共享经济
    others = Column(Integer)  # 其他
    ai = Column(Integer)  # 人工智能
    sty_enter = Column(Integer)  # 文体娱乐
    market_adver = Column(Integer)  # 营销广告
    outdoors = Column(Integer)  # 旅游户外
    realty = Column(Integer)  # 房产
    medical_health = Column(Integer)  # 医疗健康
    traffic = Column(Integer)  # 交通出行
    mobile_inter = Column(Integer)  # 移动互联网
    tools = Column(Integer)  # 工具软件
    social_real = Column(Integer)  # 社交
    edu = Column(Integer)  # 教育
    hardware = Column(Integer)  # 硬件
    game_music = Column(Integer)  # 游戏动漫
    living_consu = Column(Integer)  # 生活消费
    financial_pay = Column(Integer)  # 金融支付
    content_industry = Column(Integer)  # 内容产业
    enterprice_service = Column(Integer)  # 企业服务
    elect_business = Column(Integer)  # 电子商务
    add_time = Column(String(32))  # 数据添加时间


# 投资机构投资轮次数据
class Turn(Base):
    __tablename__ = "turn"
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(512))  # 投资机构名称
    # {value:95, name:'14.84%',round:2},
    Num_1 = Column(String(32))  # 天使轮
    Num_A = Column(String(32))  # 泛A轮
    Num_B = Column(String(32))  # 泛B轮
    Num_C = Column(String(32))  # 泛C轮
    Num_D = Column(String(32))  # D轮至Pre-IPO
    Num_Z = Column(String(32))  # 战略投资
    Num_O = Column(String(32))  # 未透露
    add_time = Column(String(32))  # 数据添加时间


# 投资机构的团队成员
class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(512))  # 投资机构名称  # 外键关联投资机构
    image = Column(String(256))  # 个人图片
    detail_url = Column(String(256))  # 详情页地址
    username = Column(String(512))  # 个人名字
    job = Column(String(512))  # 职业、头衔
    fild = Column(String(128))  # 关注投资领域
    period = Column(String(128))  # 投资阶段
    invest = Column(String(128))  # 单笔投资金额
    city = Column(String(64))  # 常驻城市
    information = Column(Text)  # 简介
    experience = Column(Text)  # 经历
    add_time = Column(String(32))  # 数据添加时间


# 机构投资案例
class Example(Base):
    __tablename__ = "example"
    id = Column(Integer, unique=True, primary_key=True)
    detail_url = Column(String(256))  # 详情页地址
    name = Column(String(512))  # 投资机构名称
    company = Column(String(512))  # 投资公司
    web = Column(String(512))  # 投资公司主页
    image = Column(String(256))  # 公司图片
    # industry_average = Column(Text)  # 行业平均数据
    money = Column(String(32))  # 投资金额
    turn = Column(String(16))  # 轮次
    vocation = Column(String(32))  # 行业
    times = Column(String(16))  # 投资时间
    add_time = Column(String(32))  # 数据添加时间


# 知名投资人
class People(Base):
    # 表名
    __tablename__ = "people"
    id = Column(Integer, unique=True, primary_key=True)
    username = Column(String(512))  # 个人名字
    image = Column(String(256))  # 人物图片
    company = Column(String(256))  # 投资机构
    detail_url = Column(String(256))

    job = Column(String(512))  # 职业、头衔
    field = Column(String(128))  # 关注投资领域
    period = Column(String(128))  # 投资阶段
    invest = Column(String(128))  # 单笔投资金额
    city = Column(String(64))  # 常驻城市
    information = Column(Text)  # 简介
    experience = Column(Text)  # 经历
    add_time = Column(String(32))  # 数据添加时间


# 创业公司
class Vcompany(Base):
    # 表名
    __tablename__ = 'vcompany'
    id = Column(Integer, unique=True, primary_key=True)
    detail_url = Column(String(256))
    image = Column(String(256))  # 公司图片
    name = Column(String(512))  # 公司名称
    all_name = Column(String(1024))  # 公司全称
    period = Column(String(32))  # 融资阶段
    field = Column(String(256))  # 创业领域
    become_time = Column(String(32))  # 成立时间
    web = Column(String(64))  # 公司官网
    place = Column(String(64))  # 公司位置
    content = Column(String(512))  # 主要服务内容
    introduction = Column(Text)  # 简介
    dynamic = Column(Text)  # 公司动态
    money_experience = Column(Text)  # 融资经历
    # 工商信息
    register_num = Column(String(64))  # 注册号
    run_status = Column(String(64))  # 经营状态
    law_represent = Column(String(64))  # 法人代表
    shareholder = Column(Text)  # 股东
    company_type = Column(String(64))  # 公司类型
    com_day = Column(String(64))  # 公司注册成立日期
    register_money = Column(String(64))  # 注册资金
    detail_place = Column(String(512))  # 公司住所
    add_time = Column(String(32))  # 数据添加时间


if __name__ == "__main__":
    engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'
                           .format(db_user, db_pawd, db_host, db_port, db_name), max_overflow=500)
    Base.metadata.create_all(engine)
