# -*- coding:utf8 -*-


from time import sleep
import pymysql
import json
from requests import Session
import sys
reload(sys)
sys.setdefaultencoding('utf8')


sqlConn = pymysql.connect(host='192.168.0.208', user='zhonglinglong', password='zll.123',db='isz_erp_npd',charset='utf8',port=3306)
sqlCursor = sqlConn.cursor()

def searchSQL(sql,type='tuple'):
    sqlCursor.execute(sql)
    if type == 'list':
        value = map(lambda x:x[0].encode('utf-8'),sqlCursor.fetchall())
        return value
    if type == 'dict':
        value = {}
        data = sqlCursor.fetchall()
        for i in data:
            try:
                value[i[0].encode('utf-8')] = i[1].encode('utf-8')
            except:
                value[i[0].encode('utf-8')] = str(i[1])
        return value
    if type == 'tuple':
        value = sqlCursor.fetchall()
        return value

class RequestsApi:
    def __init__(self):
        self.S = Session()
    def SendPost(self, url, header,datas):
        data = {
	"authTag": "4028803E60E8CE080160F3A2C1ED0058",
	"auth_code": "EA4A263F29FF586C9FC6D16A20E8C86ABD708EEE6CFAE74074727F766533FA33F12EFB25CF3B273F912CB1A096C9B9A7DBF53B27F7A7302F22E6CBBCE51E4311A8B6A1CBC7BCC2F28C611200F7166DC8EDB90287CF05CF045DCC9BE29AA5EE74F77544AB717D8433F12C269751243CE0E8F78955AB8BC8028490D40323F337D0929C8150AB3511DB1F34234446D3D8BAC71000B3BB723D189F74424EDF0E0A773D922AE7991CE199D672EB0DE067940BD69450A2D5CE334F1C234B9F868429E26F056702028732D5DD89063E463D17B0ABAD033DCF3599F1A4C370C8D8D3ECEAFB2C71054650AB26ECBE35DD2E15A30D5A78E8DC8E84B8AF5BF2B63A5A8FDCD8F4B3774B036758BB8A0DE2303BEBCA5876D1373405DA084E9A2997D113F80D2974D0567F512732FD11011F163553A206E2C6E08C9DE2CD86D80E7B2ACD3C76A7",
	"user_phone": "18279881085",
	"user_pwd": "isz123456",
	"verificationCode": "0451"
}

        self.r = self.S.post(url='http://isz.ishangzu.com/isz_base/LoginController/login.action', data=json.dumps(data), headers={"Content-Type": "application/json"})
        self.r=self.S.post(url=url,headers=eval(header),data=json.dumps(eval(datas)))
        return  self.r.json()




def add_develop_house(ApartmentData,RoomNumberData):
    "新增楼盘"
    try:
        sql = "SELECT sd.parent_id from sys_department sd INNER JOIN sys_user sur on sur.dep_id = sd.dep_id INNER JOIN sys_position spt on spt.position_id = sur.position_id " \
              "where sd.dep_district = '330100' and sd.dep_id <> '00000000000000000000000000000000' and (spt.position_name like '资产管家%' or spt.position_name like '综合管家%') " \
              "ORDER BY RAND() LIMIT 1"
        dutyDepID = searchSQL(sql)[0][0]
        header = '{ "Content-Type": "application/json", "Referer": "http://isz.ishangzu.com/isz_house/jsp/residential/residentialList.jsp"}'
        url = 'http://isz.ishangzu.com/isz_house/ResidentialController/saveResidential.action'
        data = '''{"residential_name": "%s",
	"residential_jianpin": "zllgj",
	"residential_jianpin": "csgj",
	"city_code": "330100",
	"area_code": "330102",
	"taBusinessCircleString": "5",
	"address": "工具创建楼盘",
	"gd_lng": "120.149395",
	"gd_lat": "30.298125",
	"property_type": "ordinary",
	"taDepartString": "%s",
	"build_date": "1988",
	"totle_buildings": "2",
	"total_unit_count": "200",
	"total_house_count": "1000",
	"build_area": "100.00",
	"property_company": "杭州科技有限公司",
	"property_fee": "20",
	"plot_ratio": "30.00",
	"green_rate": "100.00",
	"parking_amount": "200",
	"other_info": "楼盘亮点",
	"bus_stations": "公交站",
	"metro_stations": "地铁站","byname": "fh"}''' % (ApartmentData,dutyDepID)
        result = RequestsApi().SendPost(url, header, data)
        if result["code"] == 0:
            print ("新增楼盘名称为：'"+"%s"+"'成功！") % ApartmentData
        else:
            print result
            return
    except BaseException as e:
        print e
        return

    #新增栋座
    try:
        sql = "select residential_id from residential WHERE residential_name='%s' and deleted=0" % ApartmentData
        residentialID = searchSQL(sql)[0][0]
        header = '{ "Content-Type": "application/json", "Referer": "http://isz.ishangzu.com/isz_house/jsp/residential/residentialList.jsp"}'
        url = 'http://isz.ishangzu.com/isz_house/ResidentialBuildingController/saveResidentialBuildingNew.action'
        data = '''{
	"property_name": "%s",
	"building_name": "1幢",
	"no_building": "无",
	"gd_lng": "120.152476",
	"gd_lat": "30.287232",
	"housing_type": "ordinary",
	"ground_floors": "20",
	"underground_floors": "2",
	"ladder_count": "10",
	"house_count": "200",
	"residential_id": "%s",
	"have_elevator": "Y"}''' % (ApartmentData, residentialID)
        result = RequestsApi().SendPost(url, header, data)
        if result["code"] == 0:
            print "新增栋成功！"
        else:
            print result
            return
    except BaseException as e:
        print e
        return

    # 新增单元
    try:
        sql = "SELECT building_id  from residential_building where residential_id ='%s'and deleted=0 " % residentialID
        buildingID = searchSQL(sql)[0][0]
        header = '{ "Content-Type": "application/json", "Referer": "http://isz.ishangzu.com/isz_house/jsp/residential/residentialList.jsp"}'
        url = 'http://isz.ishangzu.com/isz_house/ResidentialBuildingController/saveResidentialBuildingUnit.action'
        data = '''{"property_name": "%s","unit_name": "A","no_unit": "无","building_id": "%s"}''' % (ApartmentData + '1幢', buildingID)
        result = RequestsApi().SendPost(url, header, data)
        if result["code"] == 0:
            print "新增单元成功！"
        else:
            print result
            return
    except BaseException as e:
        print e
        return

    # 新增楼层
    try:
        sql = "SELECT unit_id from  residential_building_unit where  building_id='%s' " % buildingID
        unitID = searchSQL(sql)[0][0]
        header = '{ "Content-Type": "application/json", "Referer": "http://isz.ishangzu.com/isz_house/jsp/residential/residentialList.jsp"}'
        url = 'http://isz.ishangzu.com/isz_house/ResidentialBuildingController/saveResidentialBuildingFloor.action'
        data = '{"property_name":"%s","floor_name":"1","building_id":"%s","unit_id":"%s"}' % (ApartmentData + '1幢A', buildingID, unitID)
        result = RequestsApi().SendPost(url, header, data)
        if result["code"] == 0:
            print "新增楼层成功！"
        else:
            print result
            return
    except BaseException as e:
        print e
        return

    # 新增房间号
    try:
        sql = "SELECT floor_id from residential_building_floor where unit_id='%s' " % unitID
        floorID = searchSQL(sql)[0][0]
        housenumber = 100
        for i in range(int(RoomNumberData)):
            housenumber = housenumber + 1
            header = '{ "Content-Type": "application/json", "Referer": "http://isz.ishangzu.com/isz_house/jsp/residential/residentialList.jsp"}'
            url = 'http://isz.ishangzu.com/isz_house/ResidentialBuildingController/saveResidentialBuildingHouseNo.action'
            data = '''{
	"property_name": "%s",
	"house_no": "%s",
	"rooms": "1",
	"livings": "1",
	"bathrooms": "1",
	"kitchens": "1",
	"balconys": "1",
	"build_area": "100.00",
	"orientation": "NORTH",
	"building_id": "%s",
	"unit_id": "%s",
	"floor_id": "%s"}''' % (ApartmentData + '1幢A1层', housenumber, buildingID, unitID, floorID)
            result = RequestsApi().SendPost(url, header, data)
            if result["code"] == 0:
                print ("新增"+"%s"+"房间成功！") % housenumber
            else:
                print result
                return
    except BaseException as e:
        print e
        return

    # 新增房源
    try:
        housenoID = []
        sql = "SELECT house_no_id  from residential_building_house_no where floor_id='%s' ORDER BY create_time " % floorID
        housenoID.append(searchSQL(sql))
        house_no = 100
        residential_name = ApartmentData + '（fh）'
        for i in range(int(RoomNumberData)):
            house_no_search = housenoID[0][i][0]
            house_no = house_no + 1
            residential_address = '杭州市 上城区 四季青 ' + ApartmentData
            url = "http://isz.ishangzu.com/isz_house/HouseController/saveHouseDevelop.action"
            header = '{ "Content-Type": "application/json", "Referer": "http://isz.ishangzu.com/isz_house/jsp/house/develop/houseDevelopinfoAdd.jsp"}'
            data = """{
	"residential_name_search": "%s",
	"building_name_search": "%s",
	"unit_search": "%s",
	"house_no_search": "%s",
	"residential_name": "%s",
	"building_name": "1幢",
	"unit": "A",
	"house_no": "%s",
	"residential_address": "%s",
	"city_code": "330100",
	"area_code": "330102",
	"business_circle_id": "35",
	"contact": "钟晓晓",
	"did": "8A215243584E2141015867FD6E1F5E9D",
	"uid": "4028803E5B196FD1015B1E5CF23C0294",
	"house_status": "WAITING_RENT",
	"category": "NOLIMIT",
	"source": "INTRODUCE",
	"rental_price": "4567.00",
	"rooms": "1",
	"livings": "1",
	"kitchens": "1",
	"bathrooms": "1",
	"balconys": "1",
	"build_area": "100",
	"orientation": "NORTH",
	"property_type": "MULTI_LIFE",
	"property_use": "HOUSE",
	"remark": "测试工具新增房源",
	"look_type": "DIRECTION",
	"residential_id": "%s",
	"building_id": "%s",
	"unit_id": "%s",
	"house_no_id": "%s",
	"business_circle_name": "四季青",
	"contact_tel": "18233669988",
	"floor": "1",
	"floor_id": "%s"}""" % (residentialID, buildingID, unitID, house_no_search, residential_name, house_no, residential_address,
        residentialID, buildingID, unitID, house_no_search, floorID)
            result = RequestsApi().SendPost(url, header, data)
            if result["code"] == 0:
                print ("新增楼盘名称：'"+"%s'下%s"+"房源成功！") % (residential_address,house_no)
            else:
                print result
                return
    except BaseException as e:
        print e
        return


    # 审核房源
    try:
        sql = 'SELECT house_develop_id from house_develop where residential_name = "%s" ORDER BY create_time and deleted=0  ' % residential_name
        sqltime = 'SELECT update_time from house_develop where residential_name = "%s" ORDER BY create_time and deleted=0 ' % residential_name
        housedevelopid = []
        update_times = []
        housedevelopid.append(searchSQL(sql))
        update_times.append(searchSQL(sqltime))
        house_no = 100
        for i in range(int(RoomNumberData)):
            update_time = update_times[0][i][0]
            house_develop_id = housedevelopid[0][i][0]
            house_no = house_no + 1
            house_no_search = housenoID[0][i][0]
            url = "http://isz.ishangzu.com/isz_house/HouseController/auditHouseDevelop.action"
            header = '{ "Content-Type": "application/json", "Referer":"http://isz.ishangzu.com/isz_house/jsp/house/develop/houseDevelopList.jsp?from=waitAudit"}'
            data = '''{
    "residential_name_search": "%s",
    "building_name_search": "%s",
    "unit_search": "%s",
    "house_no_search": "%s",
    "residential_name": "%s",
    "building_name": "1幢",
    "floor": "1",
    "house_no_suffix": "xxx",
    "residential_address": "杭州市 上城区 四季青 工具创建楼盘",
    "residential_department_did": "%s",
    "house_status": "WAITING_RENT",
    "category": "NOLIMIT",
    "rental_price": "4567.00",
    "build_area": "100.00",
    "rooms": "1",
    "livings": "1",
    "kitchens": "1",
    "bathrooms": "1",
    "balconys": "1",
    "orientation": "NORTH",
    "source": "INTRODUCE",
    "property_use": "HOUSE",
    "property_type": "MULTI_LIFE",
    "look_type": "DIRECTION",
    "remark": "测试工具新增房源",
    "houseRent": {
        "house_status": "WAITING_RENT",
        "category": "NOLIMIT",
        "source": "INTRODUCE",
        "look_type": "DIRECTION",
        "rental_price": "4567.00",
        "remark": "测试工具新增房源"
    },
    "audit_status": "PASS",
    "building_id": "%s",
    "residential_id": "%s",
    "unit_id": "%s",
    "unit": "A",
    "floor_id":"%s",
    "house_no": "%s",
    "house_no_id": "%s",
    "area_code": "330102",
    "city_code": "330100",
    "house_develop_id": "%s",
    "update_time": "%s",
    "audit_content": "同意"}''' % (residentialID, buildingID, unitID, house_no_search, residential_name,dutyDepID, buildingID, residentialID, unitID,floorID, house_no, house_no_search, house_develop_id, update_time)
            result = RequestsApi().SendPost(url, header, data)
            if result["code"] == 0:
                print ("审核杭州市 上城区 四季青 工具创建楼盘下："+"%s"+"号房间房源成功！") % house_no
            else:
                print result
                return
    except BaseException as e:
        print e
        return
    print '添加开发房源OK'


add_develop_house("新增开发房源脚本重构",3)