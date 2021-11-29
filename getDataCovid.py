import json,urllib.request

#lay du lieu tu file json cua https://covid19.gov.vn/
def getDataFromJson():
    data = urllib.request.urlopen("https://static.pipezero.com/covid/data.json").read()
    output = json.loads(data)   
    dataCovidVN = output['locations'] 
    result = []
    for row in dataCovidVN:
        tinhthanh = row['name']
        tongsoca = row['cases']
        camachomany = row['casesToday']
        tuvong = row['death']
        temp = []
        temp.append(tinhthanh)
        temp.append(tongsoca)
        temp.append(camachomany)
        temp.append(tuvong)
        result.append(temp)
    return result
    