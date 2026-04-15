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
    print("KEYS (Course):", response_dict.keys())
    
    if 'courseFlatPlan' in response_dict:
        uc = response_dict['courseFlatPlan'][0]
        print("KEYS (UC in courseFlatPlan):", uc.keys())
        
        url_uc = 'https://secure.ensinolusofona.pt/dados-publicos-academicos/resources/GetSIGESCurricularUnitDetails'
        payload_uc = {'language': language, 'curricularIUnitReadableCode': uc['curricularIUnitReadableCode']}
        response_uc = requests.post(url_uc, json=payload_uc, headers=headers)
        print("KEYS (UC Detail):", response_uc.json().keys())
        
        with open('files/sample_uc.json', 'w') as f:
            json.dump(response_uc.json(), f, indent=4)
except Exception as e:
    print("Error:", e)
