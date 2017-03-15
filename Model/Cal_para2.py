#coding=gbk
import numpy as np
import math
from scipy.optimize import leastsq
class Cal_para():
    locationList=[]
    idList=[]
    pointidList=[]
    def __init__(self,route):
        if(len(route)):
            for position in route:
                self.locationList.append([position[0],position[1]])
                self.idList.append(position[2])
            if(len(route[0])):
                for position in route:
                    self.pointidList.append(position[4])
        else:
            pass

    #��������ʱ�����ƣ��ݷõ�λ�õ������ı仯
    #���������㣬��ӳ���ǰݷõĵ�λ�������������դ�����ݣ��򷵻ص��Ƿ��ʵ�դ�������
    def get_visit_location_number(self, ids, num):
        id_array = np.array(ids[0:num])
        num = np.unique(id_array)
        return len(num)
    def get_visit_location_number_disput(self):
        #�õ�����ʱ����������ݷõĵص�������ı仯
        nums=self.set_step(2)#ѡȡ�����Ĳ�����2������100Ϊ����ͳ������
        disput=[]
        for num in nums:
            sum_number=self.get_visit_location_number(self.idList,num)
            disput.append(sum_number)
        return disput

    #��������ʱ�����ƣ�դ�������аݷõĵ�ĸ����ı仯���
    #���ҽ�������Ϊդ�����ݵ�����£����ݲŻ���ڵ���λ����
    def get_visit_location_number_raster_disput(self):
        #�õ�����ʱ����������ݷõĵص�������ı仯
        nums=self.set_step(2)#ѡȡ�����Ĳ�����2������100Ϊ����ͳ������
        disput=[]
        for num in nums:
            sum_number=self.get_visit_location_number(self.pointidList,num)
            disput.append(sum_number)
        return disput

    #��������ʱ������ۣ�rog�ı仯
    def get_Rog(self,locations,num):
        locationlist=locations[0:num]
        x=0
        y=0
        for location in locationlist:
            x+=location[0]
            y+=location[1]
        x=x/len(locationlist)
        y=y/len(locationlist)
        x2=0
        y2=0
        for location in locationlist:
            x2+=(location[0]-x)*(location[0]-x)
            y2+=(location[1]-y)*(location[1]-y)
        r=math.sqrt((x2+y2)/(len(locationlist)))
        return r
    def get_rog_disput(self):
        nums=self.set_step(1)
        disput = []
        for num in nums:
            sum_number = self.get_Rog(self.locationList, num)
            disput.append(sum_number)
        return disput

    #�õ�ѭ���������ĶȰ���������ķֲ�
    #�������ݴ�����ǵ�ķ��ʴ�����դ�����ݴ������դ����ʵ�����
    def get_weight(self, ids):
        temp1 = np.array(ids)
        temp2 = np.bincount(temp1)
        temp3 = temp2.tolist()
        temp4 = sorted(temp3, reverse=True)
        disput = []
        for temp in temp4:
            if (temp > 0):
                disput.append(temp)
        return disput
    def get_weight_disput(self):
        disputs = [0] * (int(math.log(len(self.idList)) * 3))
        disput=self.get_weight(self.idList)
        for i in range(min(len(disput),len(disputs))):
            disputs[i]=disput[i]
        return disputs

    def get_weight_raster_disput(self):
        disputs = [0] * (int(math.log(len(self.idList)) * 3))
        disput = self.get_weight(self.pointidList)
        for i in range(min(len(disput),len(disputs))):
            disputs[i]=disput[i]
        return disput

    #�õ���ͬ��դ��ı��ݷ����Ķ��٣������С�ں���Ŀ��ӻ���������Ϊ��դ��Ĵ�С
    #��Ϊդ��͵�λ����������С�ļ��㷽��
    def get_location_size(self,ids,nums):
        temp1 = np.array(ids[0:nums])
        temp2 = np.bincount(temp1)
        temp3 = temp2.tolist()
        return temp3

    def get_location_size_disput(self):
        nums=self.set_step(2)
        locations_weight=[]
        for num in nums:
            locations_weight.append(self.get_location_size(self.idList,num))
        return locations_weight

    def get_location_size_raster_disput(self):
        nums = self.set_step(2)
        locations_weight = []
        for num in nums:
            locations_weight.append(self.get_location_size(self.pointidList, num))
        return locations_weight


    # ������С���˵Ļع麯��
    def func(self, p, x):
        k, b = p
        temp_y = []
        for item in x:
            temp_y.append(k * item + b)
        return temp_y

    def error(self, p, x, y, s):
        print s
        temp_answer = []
        tempfunc = self.func(p, x)
        for i in range(0, min(len(tempfunc), len(y))):
            temp_answer.append(tempfunc[i] - y[i])
        return temp_answer

    def cal_leastsq(self, x, y):
        length = min(len(x), len(y))
        s = "Test the number of iteration"
        p0 = [100, 2]
        Para = leastsq(self.error, p0, args=(x, y, s))
        k, b = Para[0]
        return k, b

    def set_step(self,flag):
        if(flag==1):
            num1 = [j for j in range(1, int(math.log(len(self.idList), 2)) + 1)]
            nums = [int(math.pow(2, j)) for j in num1]
            return nums
        if(flag==2):
            num1 = [j for j in range(1, int((len(self.idList) / 10)) + 1)]
            nums = [int(100 * j) for j in num1]
            return nums
