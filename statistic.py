import json
import matplotlib.pyplot as plt
import datetime
from operator import itemgetter
import numpy as np
f= open("./data11.json")
data = json.load(f)
mintime = datetime.datetime(2018,1,1,1,0,0)
maxtime = datetime.datetime(2018,1,1,2,0,0)

#通过字符串长度判断时间格式是不是有问题
def is_normal(val):
    if len(val['接收时间']) < 20 and len(val['接收时间']) > 7 :
        return  True
    return False
#利用filter函数将异常时间数据删除
filter_data = list(filter(is_normal,data))
#transformed_data 用来存储将时间字符串转换为datatime格式的船舶数据
transformed_data=[]
for ship in filter_data:
    ship["纬度"]=float(ship['纬度'])
    ship['经度']=float(ship['经度'])
    ship['对地速度']=float(ship['对地速度'])
    ship["对地航向"]=float(ship["对地航向"])
    ship['船首向'] =float(ship['船首向'])
    ship['接收时间']=datetime.datetime.strptime(ship['接收时间'], '%Y-%m-%d %H:%M:%S')
    transformed_data.append(ship)
# 我们得到格式转换后的数据后，需要我们再次对异常数据进行删除，比如航向和船首向的记录度数大于350度的。
def is_right(val):
    if val['船首向']<361 and val['对地航向']<361:
        if val['对地速度']>7:
            return True
    return  False
filter_data2 = list(filter(is_right,transformed_data))
def is_angle(val):
    if val['对地航向']>275 or val['对地航向']<125:
        return True
    return False
filter_data3 = list(filter(is_angle,filter_data2))
# 将字典列表进行排序
data_by_time = sorted(filter_data3,key = itemgetter('接收时间'))
# plt.plot([x['纬度'] for x in data_by_time],[x['经度'] for x in data_by_time])
x_time=list()
y_speed=list()
angle_deviation=list()
y_angle = list()
for ship in data_by_time:
    if ship['接收时间']>mintime and ship['接收时间']<maxtime:
        x_time.append(ship['接收时间'])
        y_speed.append(ship['对地速度'])
        angle_deviation.append(ship["对地航向"]-ship['船首向'])
        y_angle.append(ship['对地航向'])
print("统计时间：",mintime,"to",maxtime,"统计了点数:",len(y_speed))
plt.subplot(2,2,1)
plt.title("angle_deviation")
plt.scatter(np.arange(len(angle_deviation)),angle_deviation)
plt.subplot(2,2,2)
plt.title("y_angle")
plt.scatter(np.arange(len(y_angle)),y_angle)
plt.subplot(2,2,3)
plt.title("y_speed")
plt.scatter(np.arange(len(y_speed)),y_speed)
# plt.yticks(np.arange(8,16,1))
# for ship in data:
#     if len(ship['接收时间'])<20 and len(ship['接收时间'])>7:
#         lat.append(float(ship["纬度"]))
#         angle.append(ship["对地航向"])
#         lng.append(float(ship['经度']))
#         ship_angle.append(ship['船首向'])
#         mmsi.append(ship['MMSI'])
#         speed.append(ship['对地速度'])
#         angle_speed.append(ship['转向速率'])
#         time.append(datetime.datetime.strptime(ship['接收时间'], '%Y-%m-%d %H:%M:%S'))
# print(lat)
# plt.plot(lng,lat)
####计算部分
up_speed=[]# 上行速度
down_speed=[]# 下行速度
up_angle =[] # 上行船的对地航向
down_angle=[] # 下行船的对地航向
up_ship_angle=[] # 上行船的船首向
down_ship_angle=[] # 下行船的船首向
lat=[]#纬度信息
lng=[]#经度信息
for ship in data_by_time:
    if ship['接收时间'] > mintime and ship['接收时间'] < maxtime:
        if ship['对地航向']>275:
            up_speed.append(ship['对地速度'])
            up_angle.append(ship['对地航向'])
            up_ship_angle.append(ship['船首向'])
            lat.append(ship['纬度'])
            lng.append(ship['经度'])
        else:
            down_speed.append(ship['对地速度'])
            down_angle.append(ship['对地航向'])
            down_ship_angle.append(ship['船首向'])
            lat.append(ship['纬度'])
            lng.append(ship['经度'])

print("上行平均速度：",np.mean(up_speed))
print("上行对地航向：",np.mean(up_angle))
print("上行行船首向：",np.mean(up_ship_angle))
print("上行角度差：",np.mean(up_angle)-np.mean(up_ship_angle))

print("下行平均速度：",np.mean(down_speed))
print("下行对地航向：",np.mean(down_angle))
print("下行行船首向：",np.mean(down_ship_angle))
print("下行角度差：",np.mean(down_angle)-np.mean(down_ship_angle))

print("上下行的速度差：",np.mean(up_speed)-np.mean(down_speed))

plt.subplot(2,2,4)
plt.title("ship_track")
plt.scatter(lng,lat)



ship_dict = {
            "上行平均速度":np.mean(up_speed),
             "上行对地航向":np.mean(up_angle),
             "上行行船首向":np.mean(up_ship_angle),
            "上行角度差":np.mean(up_angle)-np.mean(up_ship_angle),
            "下行平均速度":np.mean(down_speed),
            "下行对地航向":np.mean(down_angle),
            "下行行船首向":np.mean(down_ship_angle),
            "下行角度差":np.mean(down_angle)-np.mean(down_ship_angle),
            "上下行的速度差":np.mean(up_speed)-np.mean(down_speed)
}
# output=[]
def save_file():
    with open('./output.json') as f:
        output = json.load(f)
    output.append(ship_dict)
    with open('./output.json','w+',) as f:
        json.dump(output,f,ensure_ascii=False,indent=2)

############存储文件#########
save_file()
plt.show()

