import numpy as np


class Comfort(object):
    def __init__(self):
        self.spring = [(22.5, 79.5), (26.0, 57.3), (27.0, 19.8), (23.2, 24.4)]  # 春天时最舒适的矩形坐标
        self.summer = [(22.5, 79.5), (26.0, 57.3), (27.0, 19.8), (23.2, 24.4)]  # 夏天时最舒适的矩形坐标
        self.autumn = [(19.5, 86.5), (23.5, 58.3), (24.5, 57.3), (20.5, 29.3)]  # 秋天时最舒适的矩形坐标
        self.winter = [(19.5, 86.5), (23.5, 58.3), (24.5, 23.0), (20.5, 29.3)]  # 冬天时最舒适的矩形坐标

    def isPtInPoly_one(self, param):
        return self.isPtInPoly(param[0], param[1], param[2])

    def isPtInPoly(self, temp, hum, season=0):
        '''''
        :param temp: double 温度
        :param hum: double 湿度
        :param season: 季节
        '''
        if season == 1:
            pointList = self.spring
        elif season == 2:
            pointList = self.summer
        elif season == 3:
            pointList = self.autumn
        elif season == 4:
            pointList = self.winter
        else:
            print("请输入参数 season:0-3 ")

        iSum = 0
        iCount = len(pointList)

        if (iCount < 3):
            return False

        for i in range(iCount):

            pTemp = pointList[i][0]
            pHum = pointList[i][1]

            if (i == iCount - 1):

                pTemp2 = pointList[0][0]
                pHum2 = pointList[0][1]
            else:
                pTemp2 = pointList[i + 1][0]
                pHum2 = pointList[i + 1][1]

            if ((hum >= pHum) and (hum < pHum2)) or ((hum >= pHum2) and (hum < pHum)):

                if (abs(pHum - pHum2) > 0):

                    pLon = pTemp - ((pTemp - pTemp2) * (pHum - hum)) / (pHum - pHum2);

                    if (pLon < temp):
                        iSum += 1

        if iSum % 2 != 0:
            return 1
        else:
            return 0
