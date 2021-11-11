import requests
from bs4 import BeautifulSoup
import re, os
import pandas as pd

def gsesame2GoTerms(name):
    ## do a "post" to compare 2 go terms at g-sesame website
    # term1: 1234567 (without the GO:)
    payload = {
        "tool_id": "3",
        "isA": "0.8",
        "partOf": "0.6",
        "submit": "Submit"
    }
    url = "http://bioinformatics.clemson.edu/G-SESAME/Program/GOCompareMultiple2.php"
    files = {
        "uploadedfile1": ("uploadedfile1", open(name + "-1.txt", "rb")),
        "uploadedfile2": ("uploadedfile2", open(name + "-2.txt", "rb")),
    }
    r = requests.post(url, files=files, data=payload)
    soup = BeautifulSoup(r.text, 'html.parser')
    similarity = soup.findAll("p")  ## similarity
    similarity = similarity[0].text
    similarity = re.findall(r"\d+\.?\d*", similarity)[0]
    return (similarity)

def processing(name):
    print("processing line " + name)
    value = gsesame2GoTerms(name)
    print("similarity is " + value)
    os.remove(name + "-1.txt")
    os.remove(name + "-2.txt")
    result = name +":" + value + "\n"
    resultPath = "./result.txt"
    if not os.path.exists(resultPath):
        os.system(r"touch {}".format(resultPath))
    with open(resultPath, mode='a') as f:
        f.write(result)

def readDataFromGOPairs():
    data = pd.read_csv('GOPairs.txt', header = None, sep='\t')
    resultFile = 'result.txt'
    if os.path.exists(resultFile):
        num_lines = sum(1 for line in open(resultFile))
    else:
        num_lines = 0
    for index, row in data.iterrows():
        if index < num_lines:
            continue
        writeRowToFile(index, row.values[0], row.values[1])
        processing(str(index))

def writeRowToFile(index, string1, string2):
    writeContentToFile(index,string1,"-1.txt")
    writeContentToFile(index,string2, "-2.txt")

def writeContentToFile(index, string,fileSufix):
    tempFile = str(index) + fileSufix
    fixedString = string.replace("GO:","")
    fixedString = fixedString.replace(",", "\n")
    if os.path.exists(tempFile):
       os.remove(tempFile)
    os.system(r"touch {}".format(tempFile))
    with open(tempFile, mode='a') as f:
        f.write(fixedString)

if __name__ == '__main__':
    readDataFromGOPairs()