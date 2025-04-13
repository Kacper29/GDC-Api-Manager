import requests
import json
import re
import os

import pandas as pd
import time
import sys

def progress_bar(iteration, total, length=30):
    filled_length = int(length * iteration // total)
    bar = '\033[92m█\033[0m' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r[{bar}] {iteration}/{total}')
    sys.stdout.flush()
class GdcData:
    urlMain = "https://api.gdc.cancer.gov/"
    urlStatus = "https://api.gdc.cancer.gov/status"
    urlCases = "https://api.gdc.cancer.gov/cases"
    urlData = "https://api.gdc.cancer.gov/data"
    urlFiles = "https://api.gdc.cancer.gov/files"
    filesToPatient = dict()
    file_dict = dict()




    def __init__(self):
        pass

    def check_status(self):
        params = {"pretty": True}
        urlFinal = self.urlStatus
        response = json.loads(requests.get(urlFinal, params=params).text)
        return f"GDC API status: {response['status']}"

    def mapping(self):
        params = {"pretty": True}
        urlFinal = self.urlCases+"/_mapping"
        result = requests.get(urlFinal, params=params)
        print(json.dumps(json.loads(result.text), indent=4))








    def case_files(self, submitterID:str, dataCategory: str, size: str):
        urlFinal = self.urlFiles
        if dataCategory is None:
            filters = {
                "op": "and",
                "content": [
                    {
                        "op": "=",
                        "content": {
                            "field": "cases.submitter_id",
                            "value": submitterID
                        }
                    }
                ]
            }

        else:
            filters = {
            "op": "and",
            "content": [
                {
                    "op": "=",
                    "content": {
                        "field": "cases.submitter_id",
                        "value": submitterID
                    }
                },
                {
                    "op": "=",
                    "content": {
                        "field": "files.data_category",
                        "value": dataCategory
                    }
                }]
        }
        params = {
            "filters": json.dumps(filters),
            "pretty": True,
            "size": size
        }
        return requests.post(urlFinal, params=params, headers={"Content-Type": "application/json"})
    def cases_by(self, field, disease: str, size=10000):
        urlFinal = self.urlCases
        fields = {
            "cases.submitter_id"
        }
        filters = {
            "op": "in",
            "content": {
                "field": field,
                "value": disease

            }
        }
        params = {
            "fields": fields,
            "pretty": True,
            "filters": json.dumps(filters),
            "size": size
        }
        return requests.get(urlFinal, params=params)

    def download_file(self, fileIDs: list, directory: str, PatientID, data_type: list):
        os.makedirs(directory, exist_ok=True)
        file_counter = pd.DataFrame()


        bar_iter = 0
        for fileID in range(len(fileIDs)):
            try:
                print(range(len(fileIDs)-1))
                data_endpt = "https://api.gdc.cancer.gov/data/{}".format(fileIDs[fileID])
                response = requests.get(data_endpt, headers={"Content-Type": "application/json"})
                print(response)
                response_head_cd = response.headers["Content-Disposition"]
                print(response_head_cd)
                file_name = re.findall("filename=(.+)", response_head_cd)[0]
                file_path = os.path.join(directory, data_type[fileID], PatientID + "_" + file_name)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "wb") as output_file:
                    output_file.write(response.content)

                print(f"\nFile {fileID} has been successfully downloaded and saved")




                bar_iter += 1
                progress_bar(bar_iter, len(fileIDs))

            except KeyError:
                print(f"\033[91mWarning\033[0m: File {fileID} is not accessible without an API token")
                progress_bar(bar_iter, len(fileIDs))



    def check_access(self, val):
        if val == 'open':
            return True
        else:
            return False
    def full_file_request(self, field, search_parameter:str, file_type:str, size=10000):
        diseaseFile = search_parameter.replace(" ", "_")
        diseasetypeFile = file_type.replace(" ", "_")
        directory = diseaseFile+"/"+diseasetypeFile
        os.makedirs(directory, exist_ok=True)
        cases = pd.DataFrame.from_dict(self.cases_by(field, search_parameter, size).json()['data']['hits'])
        cases.to_csv(directory+"/"+"cases.csv")
        IDlist = cases['submitter_id'].tolist()



        # PatientID = 1
        filecount = pd.DataFrame(index=IDlist)

        for i in IDlist:
            try:
                file = pd.DataFrame.from_dict(self.case_files(i, file_type, 10000).json()['data']['hits'])
                file.to_csv(directory + "/" + "files" + str(i) + ".csv")



                fileID = file['file_id'].tolist()
                dataType = file['data_type'].tolist()
                ifControlled = file['access'].tolist()
                ifControlled = [self.check_access(x) for x in ifControlled]

                to_pop = []
                for j in range(len(ifControlled)):

                    if ifControlled[j]:
                        pass
                    else:
                        to_pop.append(j)
                for j in sorted(to_pop, reverse=True):
                    dataType.pop(j)
                    fileID.pop(j)

                for data in dataType:
                    filecount.loc[i, data] = True


                patients_data_category = {i: {i for i in dataType}}




                print(len(fileID))
                self.download_file(fileID, directory, str(i), dataType)
            except:
                print("Submitter id not valid")


            # PatientID += 1



        filecount.to_csv(directory+"/testyzliczania.csv")












