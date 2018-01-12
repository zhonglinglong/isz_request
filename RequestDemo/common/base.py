# -*- coding:utf8 -*-
# Author : Zhong Ling Long
# Create on : 2017 - 12 -25

import logging
import ConfigParser
import pymysql
from xlrd import open_workbook
from run import *


logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
path = os.path.dirname(
    os.path.join(
        os.path.split(
            os.path.realpath(__file__))[0])) + '\\test.log'
fileHandler = logging.FileHandler(path)
consoleHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(process)s - %(levelname)s : %(message)s')
fileHandler.setFormatter(formatter)
consoleHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)




def log(func):
    def wrapper(*args, **kwargs):
        logger.info(func.__doc__)
        try:
            return func(*args, **kwargs)
        except BaseException as e:
            return e
    return wrapper



def consoleLog(msg, level='i'):
    """
    对错误的记录，写进log文件中
    则调用此方法，定义为error级别
    :param msg: 需要写入的描述，如’合同删除后deleted未变成0‘
    :param level: 定义日志级别，分为i:info  w:warning  e:error
    """
    if level is 'i':
        logger.info(msg)
    elif level is 'w':
        logger.warning(msg)
    elif level is 'e':
        logger.error('one assert at : \n%s\n' % msg)

def get_conf(section, option, valueType=str):
    """
    获取配置文件值
    :param section: 配置文件的片段
    :param option: 配置文件对应的key
    :param valueType: 默认值
    :return:
    """
    config = ConfigParser.ConfigParser()
    path = os.path.join(os.path.split(os.path.realpath(__file__))[0]) + '\conf.ini'
    config.read(path)
    if valueType is str:
        value = config.get(section, option)
        return value
    elif valueType is int:
        value = config.getint(section, option)
        return value
    elif valueType is bool:
        value = config.getboolean(section, option)
        return value
    elif valueType is float:
        value = config.getfloat(section, option)
        return value
    else:
        value = config.get(section, option)
        return value.decode('utf-8')


def set_conf(section, **value):
    """
    写入值到配置文件中
    :param section: 配置文件中的片段名称
    :param value: 配置文件中的key
    :return:
    """
    config = ConfigParser.ConfigParser()
    path = os.path.join(os.path.split(os.path.realpath(__file__))[0]) + '\conf.ini'
    config.read(path)
    for k,v in value.items():
        if type(v) is unicode:
            config.set(section,k,v.encode('utf-8'))
        else:
            config.set(section, k, v)
    config.write(open(path, 'w'))



conn = pymysql.connect(host=get_conf('db','host'), user=get_conf('db','user'), password=get_conf('db','password'), db=get_conf('db','db'), charset=get_conf('db','charset'), port=get_conf('db','port',int))
cursor = conn.cursor()


def serach(sql,needConvert = True,oneCount = True):
    """
    返回查询结果
    :param sql: 查询sql
    :param needConvert: 转换为Unicode、int以及datetime之类的时间数据
    :param oneCount: 返回结果是单条还是多条
    :return:list格式的查询结果
    """
    cursor.execute(sql)
    conn.commit()
    def convert(data):
        if type(data[0]) is tuple:
            if len(data[0]) == 1:
                return [i for i in data]
        elif data is None:
            consoleLog(u'查询无结果')
            return data
        for x, y in enumerate(data):
            if type(data[x]) is tuple or type(data[x]) is list:
                data[x] = list(y)
                convert(data[x])
        return data
    try:
        value = convert(list(cursor.fetchone()) if oneCount else list(cursor.fetchall()))
    except TypeError,e:
        consoleLog(e.message + '\n' + u'当前执行sql：%s' % sql.decode('utf-8'),level='e')
    else:
        if needConvert:
            if value is None:
                consoleLog(u'查询无结果')
                return value
            else:
                for x in range(len(value)):
                    if type(value[x]) is not list:
                        if type(value[x]) is not unicode and type(value[x]) is not int:
                            value[x] = str(value[x])
                    else:
                        for y in range(len(value[x])):
                            if type(value[x][y]) is not unicode and type(value[x][y]) is not int:
                                value[x][y] = str(value[x][y])
                return value
        else:
            return value


def get_xlrd(xls_name,xls_sheet):
    """
    :param xls_name: 用例表格名称
    :param xls_sheet: 用例表格页签名称
    :return:
    """
    "read xled"
    # route = os.path.abspath(name+".xlsx")
    # workbook = xlrd.open_workbook(route)
    # return workbook.sheet_names()
    cls = []
    xlsPath = os.path.join(get_conf("caseroute","path"), "caseFile",  xls_name)
    print xlsPath
    file = open_workbook(xlsPath)
    sheets = file.sheet_by_name(xls_sheet)
    nrows = sheets.nrows
    for i in range(nrows):
        if sheets.row_values(i)[0] != u'case_name':
            cls.append(sheets.row_values(i))
    return cls



