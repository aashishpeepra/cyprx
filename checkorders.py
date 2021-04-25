from worksheet import readEntireData
def extract(each):
    return [each[2],float(each[3]),int(each[4]),float(each[5]),float(each[6])]
data = list(readEntireData())[1:]
data = data[::-1]
data=data[3:]
data = list(map(extract,data))
sells = []
buys = []
feeu = 0
feed = 0
current = 0
length = len(data)
# print(data)
doges = 0
for i in range(length-1):
    BUY = data[i]
    SELL = data[i+1]
    cp = data[i][1]
    sp = data[i+1][1]
    ci = data[i][2]
    si = ci
    pc = round(ci*cp,7)
    ps = round(si*sp,7)
    extra = (ci-data[i+1][2])*SELL[1]
    doges+=BUY[2]-SELL[2]
    print("{} - {} = {}".format(ci,SELL[2],BUY[2]-SELL[2]))
    print("{} - {} = {}".format(pc,ps, round(ps-pc,7)   )   ) 
    print("{} - {} + {} = {}".format(SELL[3],BUY[3],extra,round(SELL[3]-BUY[3] +extra ,7)))
    print("*"*18)

for each in data:
    if each[0] == "SELL":
        feeu+=float(each[4])
        sells.append(each)
    else:
        feed+=float(each[4])
        buys.append(each)
sellSum = sum(list(map(lambda a:float(a[3]),sells)))
buySum = sum(list(map(lambda a:float(a[3]),buys)))
print("SELL TOTAL ",sellSum)
print("BUY TOTAL ",buySum)
print("PROFIT ",round(sellSum-buySum + doges*0.279 - round(feeu,7),7))
print("FEE u : ",feeu)
print("fee d : ",feed)
print("doges left : ",doges-feed) 