import pandas as pd
from GPRM_model import GPRM
#arizona 15 7
#ca 15 7
#nm 15 4
#tx 15 6
df = pd.read_csv("tx.csv")   #data feeded
"""
TEACB = df["TEACB"]
TECCB = df["TECCB"]
TEICB = df["TEICB"]
TERCB = df["TERCB"]
CLTCB = df["CLTCB"]
HYTCB = df["HYTCB"]
KSTCB = df["KSTCB"]
LGTCB = df["LGTCB"]
MGTCB = df["MGTCB"]
NGTCB = df["NGTCB"]
NUETB = df["NUETB"]
SOTCB = df["SOTCB"]
WWTCB = df["WWTCB"]
WYTCB = df["WYTCB"]
"""


SF = df["SF"] * 0.8
SG = df["SG"] * 1.2
caData = [SF, SG]
for i in range(len(caData)):
    l = len(SF)
    if i == 0:
        name = "SF"
    else:
        name = "SG"
    for p in range(len(caData[i])):
        if p >= 4:
            caData[i][p] = (caData[i][p] + caData[i][p - 1] + caData[i][p - 2] + caData[i][p - 3] + caData[i][p - 4]) / 5

    Predictor = GPRM(caData[i][l - 15:], 2000, 2050)
    prediction = Predictor.predictWithRM()
    print("in 2050, the predicted number for ", name, " is ", prediction)
    Predictor = GPRM(caData[i][l - 15:], 2000, 2025)
    prediction = Predictor.predictWithRM()
    print("in 2025, the predicted number for ", name, " is ", prediction)
    Predictor.alpha = 0.8
    errorRate = Predictor.errorRate()
    print("for ", name, " the error rate is ", errorRate)
