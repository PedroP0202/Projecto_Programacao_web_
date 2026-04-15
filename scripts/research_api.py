import requests, json, os

schoolYear = '202526'
course = 260      # LEI
language = 'PT'

url = 'https://secure.ensinolusofona.pt/dados-publicos-academicos/resources/GetCourseDetail'
payload = {'language': language, 'courseCode': course, 'schoolYear': schoolYear}
headers = {'content-type': 'application/json'}

print(f"Fetching Course {course} detail...")
response = requests.post(url, json=payload, headers=headers)
response_dict = response.json()

with open("files/course_sample.json", "w", encoding="utf-8") as f:
    json.dump(response_dict, f, indent=4)

if 'courseFlatPlan' in response_dict and len(response_dict['courseFlatPlan']) > 0:
    uc = response_dict['courseFlatPlan'][0]
    print(f"Fetching UC {uc['curricularUnitName']} detail...")
    url_uc = 'https://secure.ensinolusofona.pt/dados-publicos-academicos/resources/GetSIGESCurricularUnitDetails'
    payload_uc = {'language': language, 'curricularIUnitReadableCode': uc['curricularIUnitReadableCode']}
    response_uc = requests.post(url_uc, json=payload_uc, headers=headers)
    with open("files/uc_sample.json", "w", encoding="utf-8") as f:
        json.dump(response_uc.json(), f, indent=4)
