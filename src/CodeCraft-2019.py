import logging
import sys
from collections import OrderedDict
#导入最优路径算法模块
import  shortest_path
#导入交通流分配模块
import go_path

logging.basicConfig(level=logging.DEBUG,
                    #filename='../logs/CodeCraft-2019.log',
                    filename='../../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


def main():
    # if len(sys.argv) != 5:
    #   logging.info('please input args: car_path, road_path, cross_path, answerPath')
    #   exit(1)
    # sys.argv 是获取运行python文件的时候命令行参数，且以list形式存储参数
    # sys.argv[0] 代表当前module的名字
    # car_path = sys.argv[1]
    # road_path = sys.argv[2]
    # cross_path = sys.argv[3]
    # answer_path = sys.argv[4]

    car_path = '../config/car.txt'
    road_path = '../config/road.txt'
    cross_path = '../config/cross.txt'
    answer_path = '../config/answer.txt'

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))

    # to read input file
    carlist = read_txtdata("car", car_path)
    roadlist = read_txtdata("road", road_path)
    crosslist = read_txtdata("cross", cross_path)

    # buinding data to dictlist
    cardictlist = buinding_data("car", carlist)
    roaddictlist = buinding_data("road", roadlist)
    crossdictlist = buinding_data("cross", crosslist)

    # routing algorithm
    # traffic rules
    # 生成道路网络字典
    roadnet_list = road_init(roaddictlist)
    #最短路径-Dijkstra
    short_path = shortest_path.dijkstra(len(crossdictlist),crosslist, roadnet_list)
    #计算所有车辆的最优路径
    cars_path = {}
    for i in range(len(cardictlist)):
        fromid = str(int(cardictlist[i]['fromid']))
        toid = str(int(cardictlist[i]['toid']))
        path = fromid + '->' + toid
        temp_list = []
        temp_list.append(int(cardictlist[i]['speed']))
        temp_list.append(int(cardictlist[i]['plantime']))
        car_path  = str(int(cardictlist[i]['carid'])) + ':' + path
        cars_path[car_path] = short_path[path] + temp_list

    # 车辆按交通规则出发,分配交通流
    # 按照时间片进行分配
    roadnet_list=go_path.cars_go_path(roadnet_list,cars_path)
    print(roadnet_list)

    # to write output file


#  read_txtdata function
def read_txtdata(data_type, path):
    if data_type == "car":
        with open(path) as file_obj:
            datalist = file_obj.readlines()
        datalist.pop(0)
        i = 0
        for keys in datalist:
            keys_1 = keys.split('\n')[0]
            keys_2 = keys_1.split('(')[1]
            datalist[i] = keys_2.split(')')[0]
            i += 1
        logging.info("cartxt read  success !")
        return datalist
    if data_type == "road":
            with open(path) as file_obj:
                datalist = file_obj.readlines()
            datalist.pop(0)
            i = 0
            for keys in datalist:
                keys_1 = keys.split('\n')[0]
                keys_2 = keys_1.split('(')[1]
                datalist[i] = keys_2.split(')')[0]
                i += 1
            logging.info("roadtxt read  success !")
            return datalist
    if data_type == "cross":
            with open(path) as file_obj:
                datalist = file_obj.readlines()
            datalist.pop(0)
            i = 0
            for keys in datalist:
                keys_1 = keys.split('\n')[0]
                keys_2 = keys_1.split('(')[1]
                datalist[i] = keys_2.split(')')[0]
                i += 1
            logging.info("crosstxt read  success !")
            return datalist

#  buinding_data function
def buinding_data(data_type, datalist):
    # car data buinding to cardict
    if data_type=="car":
        cardictlist = []
        # cardict=OrderedDict(carid='0',formid='0',toid='0',speed='0',plantime='0')
        for i in range(len(datalist)):
            cardict = dict(
                            carid='0',
                            fromid='0',
                            toid='0',
                            speed='0',
                            plantime='0')
            car = datalist[i].split(',')
            cardict['carid'] = car[0]
            cardict['fromid'] = car[1]
            cardict['toid'] = car[2]
            cardict['speed'] = car[3]
            cardict['plantime'] = car[4]
            cardictlist.append(cardict)
        return  cardictlist
        # print(cardictlist)

    # road data buinding to roaddict
    if data_type == "road":
        roaddictlist = []
        # roaddict=OrderedDict(carid='0',formid='0',toid='0',speed='0',plantime='0')
        for i in range(len(datalist)):
            roaddict = dict(
                             roadid='0',
                             roadlength='0',
                             roadspeed='0',
                             roadchannel='0',
                             fromid='0',
                             toid='0',
                             isDuplex='0')
            road = datalist[i].split(',')
            roaddict['roadid'] = road[0]
            roaddict['roadlength'] = road[1]
            roaddict['roadspeed'] = road[2]
            roaddict['roadchannel'] = road[3]
            roaddict['fromid'] = road[4]
            roaddict['toid'] = road[5]
            roaddict['isDuplex'] = road[6]
            roaddictlist.append(roaddict)
        return roaddictlist

    # cross data buinding to crossdict
    if data_type == "cross":
        crossdictlist = []
        # crossdict=OrderedDict(carid='0',formid='0',toid='0',speed='0',plantime='0')
        for cross_1 in datalist:
            crossdict = dict(
                              crossid='0',
                              roadid1='0',
                              roadid2='0',
                              roadid3='0',
                              roadid4='0')
            cross = cross_1.split(',')
            crossdict['crossid'] = cross[0]
            crossdict['roadid1'] = cross[1]
            crossdict['roadid2'] = cross[2]
            crossdict['roadid3'] = cross[3]
            crossdict['roadid4'] = cross[4]
            crossdictlist.append(crossdict)
        return crossdictlist
        # print(crossdictlist)


#  道路初始化
def road_init(roadlist):
    roadnet_list=OrderedDict({})
    for i in range(len(roadlist)):
        road_initlist = []  # 道路初始化
        road_rows = [0] * int(roadlist[0]["roadlength"])
        roadnet1_list = {'direct': '0', 'roadlength': '0', 'speed': '0', 'fromid': '0', 'toid': '0','rlist': []}  # 网络字典，方向：1-正向，-1-反向
        roadnet1_list = OrderedDict(roadnet1_list)
        roadnet2_list = {'direct': '0', 'roadlength': '0', 'speed': '0', 'fromid': '0', 'toid': '0',
                         'rlist': []}  # 网络字典，方向：1-正向，-1-反向
        roadnet2_list = OrderedDict(roadnet2_list)
        for j in range(int(roadlist[i]["roadchannel"])):
            road_initlist.append(road_rows)
        roadnet1_list['rlist'] = road_initlist
        roadnet1_list['direct'] = roadlist[i]["isDuplex"]
        roadnet1_list['speed'] = roadlist[i]["roadspeed"]
        roadnet1_list['fromid'] = roadlist[i]['fromid']
        roadnet1_list['toid'] = roadlist[i]["toid"]
        roadnet1_list['roadlength'] = roadlist[i]["roadlength"]
        roadnet2_list['rlist'] = road_initlist
        roadnet2_list['direct'] = roadlist[i]["isDuplex"]
        roadnet2_list['speed'] = roadlist[i]["roadspeed"]
        roadnet2_list['roadlength'] = roadlist[i]["roadlength"]
        if int(roadlist[i]["isDuplex"]) == 1:
            #roadnet_list[roadlist[i]["roadid"]+':'+roadlist[i]['fromid']+'->'+str(int(roadlist[i]["toid"]))] = roadnet1_list
            roadnet_list[str(int(roadlist[i]['fromid'])) + '->' + str(int(roadlist[i]["toid"]))] = roadnet1_list
            roadnet2_list['fromid'] = roadlist[i]['toid']
            roadnet2_list['toid'] = roadlist[i]["fromid"]
            #roadnet_list[roadlist[i]["roadid"]+':'+roadlist[i]['toid']+'->'+str(int(roadlist[i]["fromid"]))] = roadnet2_list
            roadnet_list[str(int(roadlist[i]['toid']))+ '->' + str(int(roadlist[i]["fromid"]))] = roadnet2_list
        else:
            #roadnet_list[roadlist[i]["roadid"] + ':'+roadlist[i]['fromid']+'->'+str(int(roadlist[i]["toid"]))] = roadnet1_list
            roadnet_list[str(int(roadlist[i]['fromid'])) + '->' + str(int(roadlist[i]["toid"]))] = roadnet1_list
    return roadnet_list


if __name__ == "__main__":
    main()