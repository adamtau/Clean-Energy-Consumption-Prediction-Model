import numpy as np
import math


class GPRM:
    """The Grey Prediction with Rolling Mechanisms model used to predict energy prediction"""
    def __init__(self, predictionList, year, targetYear):
        self.predictionData = list(predictionList)
        self.alpha = 0.5
        self.mape = 0
        self.errorPredict = 0
        self.windowsize = 6
        self.errorPredictHelper = 1
        self.year = year
        self.targetYear = targetYear



    def AGO(self, dataList):
        """
        :param dataList: a list of data. for example, prediction data, parameter data, etc
        :return: the data list after 1 - AGO
        """
        afterAgo = []
        for i in range(len(dataList)):
            oneDataPoint = 0
            for m in range(i + 1):
                oneDataPoint += dataList[m]
            afterAgo.append(oneDataPoint)
        assert len(afterAgo) == len(dataList), "AGO shouldn't change the list size!"
        assert afterAgo[0] == dataList[0], "X1[0] should equal X0[0]!"
        assert abs(afterAgo[2] - afterAgo[1] - dataList[2]) < 0.001, "before ago, the list is " + str(dataList) + \
                                                         " after ago, the list is " + str(afterAgo)
        return afterAgo

    def leastSquare(self, A, B):
        """
        :param A: a matrix
        :param B: a vector
        :return: a vector of least squaring matri a and b
        """
        return np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(A), A)), np.transpose(A)), B)

    def predictWithoutRM(self, dataList, k):
        """
        the main process of GP without RM
        predict k + 1 value
        :return: a number representing the predicted value (x0 (k+1))
        """
        def zOne(k):
            return self.alpha * xOne[k] + (1-self.alpha) * xOne[k-1]
        xOne = self.AGO(dataList)
        n = len(dataList)
        B = np.array([
            [-zOne(1), 1]
        ])
        for i in range(2, n):
            newRow = [-zOne(i), 1]
            B = np.vstack([B, newRow])
        #print("B is ", B)
        Y = np.array(dataList[1:])
        #print("Y is ", Y)
        a, b = self.leastSquare(B, Y)
        if self.errorPredict == 0:
            self.errorPredict += 0.5 * a
        return (1 - math.e ** a) * (dataList[0] - b / a) * (math.e ** (-a * k))

    def predictWithRM(self):
        d = self.predictionData[:self.windowsize]
        # print("length of prediction data is ", len(self.predictionData))

        for k in range(self.targetYear - self.year):
            # d = self.predictionData[k-3 : k+1]
            # print("d is ", d)
            for i in range(len(d)):
                if d[i] == 0:
                    d[i] = 0.01
            predicated = self.predictWithoutRM(d, self.windowsize) - self.errorPredict
            # if self.predictionData[k + 1] == 0:
            #    self.predictionData[k + 1] = 0.01
            # self.mape += abs(predicated - self.predictionData[k + 1]) / self.predictionData[k + 1]
            # print("predicated is ", predicated, " the corresponding is ", self.predictionData[k + 1])
            # print("the first one should be 0.0575", self.mape)
            d.append(predicated)
            self.year += 1
            # d.append(self.predictionData[k+1])
            d = d[1:]

        if self.year == self.targetYear:
            return d[-1]
        else:
            return "Something Wrong, now is " + str(self.year) + ", but target is " + str(self.targetYear)

        # self.mape / (len(self.predictionData) - self.windowsize)
    def errorRate(self):
        d = self.predictionData[:self.windowsize]
        #print("length of prediction data is ", len(self.predictionData))

        for k in range(self.windowsize - 1, len(self.predictionData) - 1):
            #d = self.predictionData[k-3 : k+1]
            #print("d is ", d)
            for i in range(len(d)):
                if d[i] == 0:
                    d[i] = 0.01
            predicated = self.predictWithoutRM(d, self.windowsize) - self.errorPredict
            if self.predictionData[k + 1] == 0:
                self.predictionData[k + 1] = 0.01
            if self.predictionData[k + 1] < 0:
                print("waht the fuck?", self.predictionData[k + 1])
            self.mape += abs(predicated - self.predictionData[k + 1]) / self.predictionData[k + 1]
            #print("predicated is ", predicated, " the corresponding is ", self.predictionData[k + 1])
            #print("the first one should be 0.0575", self.mape)
            d.append(predicated)
            self.year += 1
            #d.append(self.predictionData[k+1])
            d = d[1:]
        e = self.mape / (len(self.predictionData) - self.windowsize)
        #if e < 0:
         #   print("mape is ", self.mape)
         #   print("data size minus windowsize is ", (len(self.predictionData) - self.windowsize))
        return e


#test = [264.74, 288.78, 317.38, 337.20, 345.86, 403.27, 430.4, 454.26, 482.94, 501.2, 559.42, 592.99, 645.71,
#       745.97, 821.44, 921.97]
#t1 = GPRM(test, 1, 1)
#print(t1.predictWithRM())
"""
d = self.predictionData[:self.windowsize]
        #print("length of prediction data is ", len(self.predictionData))

        for k in range(self.targetYear - self.year):
            #d = self.predictionData[k-3 : k+1]
            #print("d is ", d)
            for i in range(len(d)):
                if d[i] == 0:
                    d[i] = 0.01
            predicated = self.predictWithoutRM(d, self.windowsize) - self.errorPredict
            #if self.predictionData[k + 1] == 0:
            #    self.predictionData[k + 1] = 0.01
            #self.mape += abs(predicated - self.predictionData[k + 1]) / self.predictionData[k + 1]
            #print("predicated is ", predicated, " the corresponding is ", self.predictionData[k + 1])
            #print("the first one should be 0.0575", self.mape)
            d.append(predicated)
            self.year += 1
            #d.append(self.predictionData[k+1])
            d = d[1:]

        if self.year == self.targetYear:
            return d[-1]
        else:
            return "Something Wrong, now is " + str(self.year) + ", but target is " + str(self.targetYear)


        #self.mape / (len(self.predictionData) - self.windowsize)
"""

"""
        d = self.predictionData[:self.windowsize]
        #print("length of prediction data is ", len(self.predictionData))

        for k in range(self.windowsize - 1, len(self.predictionData) - 1):
            #d = self.predictionData[k-3 : k+1]
            #print("d is ", d)
            for i in range(len(d)):
                if d[i] == 0:
                    d[i] = 0.01
            predicated = self.predictWithoutRM(d, self.windowsize) - self.errorPredict
            if self.predictionData[k + 1] == 0:
                self.predictionData[k + 1] = 0.01
            self.mape += abs(predicated - self.predictionData[k + 1]) / self.predictionData[k + 1]
            #print("predicated is ", predicated, " the corresponding is ", self.predictionData[k + 1])
            #print("the first one should be 0.0575", self.mape)
            d.append(predicated)
            self.year += 1
            #d.append(self.predictionData[k+1])
            d = d[1:]

        return self.mape / (len(self.predictionData) - self.windowsize)
"""