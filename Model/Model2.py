#coding=gbk
import coorditinates
import powerlow
import math
import random
class Model():
    args_model = []
    args_step = []
    args_t = []
    args_coordition = []
    simulate_time = 0
    # ��ʼ������
    # args_model������������S��p����ָ��gama
    # args_t������������ʱ���ָ����������,Ҫģ��Ľ������
    # args_step ������������Ϣ��ָ��������
    # args_grid ����Ĳ������������񡾳�������������������̫�ֲ��������ɲ��������õ��ĵ�ĸ���
    grid=[]
    locations=[]
    steps = []
    ts = []
    # �ڳ�ʼ�����ݸ����������𽥱���ֵ�Ĳ���
    ids = []
    frequency = []
    start_position=[]

    # ��Ҫ���·��������Ĳ���
    def __init__(self, args_model, args_step, args_t, args_grid, simulate_time):
        self.args_grid = args_grid
        self.args_model = args_model
        self.args_step = args_step
        self.args_t = args_t
        self.simulate_time = simulate_time
        self.set_t()
        self.set_grid()
    def get_route(self):
        if(self.grid!=0):
            L_place = [item for item in self.locations]  # û�з��ʵļ���
        else:
            exit()
        L_tempPlace = []  # ���ʵļ���
        gama = self.args_model[2]
        S = self.args_model[0]
        r = self.args_model[1]
        # ���ѡ����ʼ�㣬����ʼ����Ҫ�õ���ѭ������
        postion = random.choice(L_place)
        L_tempPlace.append(postion)
        L_place.remove(postion)
        self.start_position=postion
        S = S + 1
        index = 0
        time_sum = 0
        while ((time_sum < self.simulate_time) & (index < len(self.ts) - 1)):
            tag = r * S ** (gama)
            tag2 = random.random()
            if (tag > tag2):
                # ��ʱ��ȥ̽���µĳ�������
                next_postion = self.get_next_position(postion, L_place)
                if (next_postion == 0):
                    continue
                postion = next_postion
                ##���µ�ǰ����
                L_tempPlace.append(postion)
                L_place.remove(postion)
                S = S + 1
                index = index + 1
            else:
                postion = random.choice(L_tempPlace)
                L_tempPlace.append(postion)
                index = index + 1
            time_sum = time_sum + self.ts[index]
        for tempPlace in L_tempPlace:
            self.ids.append(tempPlace[2])
        return L_tempPlace

    def get_next_position(self):
        pass

    def set_grid(self):
        pass
    def set_t(self):
        if (len(self.args_t) != 0):
            self.ts = powerlow.get_float_powerlaw(self.args_t[0], self.args_t[1], self.args_t[2], self.args_t[3])


class Normal_Model(Model):
    def dis(self,temp1,temp2):
        return math.pow((temp1[0]-temp2[0]),2)+math.pow((temp1[1]-temp2[1]),2)
    def set_grid(self):
        if (len(self.args_grid) == 3):
            temp = coorditinates.normal_raster(self.args_grid[0], self.args_grid[1], self.args_grid[2])
            self.grid=temp.grid
            self.locations=temp.locationList
        else:
            print 'grid args is wrong'
    def get_next_position(self,postion,L_place):
        # ����p=size/pow(d.beta)
        beta = self.args_step[0]
        max_step = self.args_step[1]
        gridDimension = self.args_grid[0]
        psum = []
        temp_sum = 0
        temp_positon = []
        # �ڰ뾶�ڵ���������������x��y֮��
        for p in L_place:
            dis=self.dis(postion, p)
            if(dis<max_step*max_step):
                temp_positon.append([p,dis])
        temp2 = []
        for t_p in temp_positon:
            if (t_p[1] > 0):
                p = t_p[0][3]*pow(t_p[1], beta)
                temp_sum = temp_sum + p
                psum.append(temp_sum)
        if (len(psum) > 0):
            ptemp = random.uniform(0, psum[len(psum) - 1])
            nextstep = None
            for index, temp in enumerate(psum):
                if (ptemp < temp):
                    nextstep = temp_positon[index]
                    break
            return nextstep[0]
        else:
            return 0

class Random_Model(Normal_Model):
    def set_grid(self):
        if (len(self.args_grid) == 3):
            temp = coorditinates.random_raster(self.args_grid[0], self.args_grid[1], self.args_grid[2])
            self.grid=temp.grid
            self.locations=temp.locationList
        else:
            print 'grid args is wrong'
class PowerLaw_grid_Model(Normal_Model):
    def set_grid(self):
        if (len(self.args_grid) == 3):
            temp = coorditinates.powerLaw_grid(self.args_grid[0], self.args_grid[1], self.args_grid[2])
            self.grid = temp.grid
            self.locations = temp.locationList
        else:
            print 'grid args is wrong'

class Simple_grid_Model(Normal_Model):
    def set_grid(self):
        if (len(self.args_grid) == 3):
            temp = coorditinates.simple_grid(self.args_grid[0], self.args_grid[2])
            self.grid = temp.grid
            self.locations = temp.locationList
        else:
            print 'grid args is wrong'


class ExReModel(Model):
    def set_grid(self):
        if(len(self.args_grid==3)):
            temp=coorditinates.powerlaw_grid(self.args_grid[0],self.args_grid[1],self.args_grid[2])
            self.grid=temp.grid
            self.locations=temp.locationList
        else:
            print '��������ϵ�����в��������Ƿ������ģ�Ͳ���Ū��'


