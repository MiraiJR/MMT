import json,urllib.request

class tinhThanh:
    def __init__(self, name, cases, casesToday, death):
        self.name = name
        self.cases = cases
        self.casesToday = casesToday
        self.death = death


#lay du lieu tu file json cua https://covid19.gov.vn/
def getDataFromJson():
    data = urllib.request.urlopen("https://static.pipezero.com/covid/data.json").read()
    output = json.loads(data)   
    dataCovidVN = output['locations'] 
    List = []
    for row in dataCovidVN:
        temp = tinhThanh(row['name'], row['cases'], row['casesToday'], row['death'])
        List.append(temp.__dict__)
    return List

def writeDataToJson(nameFile, list):
    with open(nameFile, 'w') as outfile:
        json.dump(list, outfile, indent=4)
        
def readDataFromJson(nameFile):
    with open(nameFile) as f_in:
        return json.load(f_in)