import requests, json, os

schoolYear = '202526'
course = 260      # LEI
language = 'PT'

url = 'https://secure.ensinolusofona.pt/dados-publicos-academicos/resources/GetCourseDetail'
payload = {'language': language, 'courseCode': course, 'schoolYear': schoolYear}
headers = {'content-type': 'application/json'}

try:
    response = requests.post(url, json=payload, headers=headers)
    response_dict = response.json()
    print("Course Detail keys:", response_dict.keys())
    if 'courseFlatPlan' in response_dict:
        print("First UC keys:", response_dict['courseFlatPlan'][0].keys())
        uc = response_dict['courseFlatPlan'][0]
        url_uc = 'https://secure.ensinolusofona.pt/dados-publicos-academicos/resources/GetSIGESCurricularUnitDetails'
        payload_uc = {'language': language, 'curricularIUnitReadableCode': uc['curricularIUnitReadableCode']}
        response_uc = requests.post(url_uc, json=payload_uc, headers=headers)
        print("Detailed UC keys:", response_uc.json().keys())
except Exception as e:
    print("Error:", e)
