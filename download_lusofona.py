import requests, json, os
schoolYear = '202526'

course = 260      # LEI

for language in ['PT', 'ENG']:

    url = 'https://secure.ensinolusofona.pt/dados-publicos-academicos/resources/GetCourseDetail'

    # Define the payload data to be sent in the POST request
    payload = {
        'language': language,
        'courseCode': course,
        'schoolYear': schoolYear
    }

    # Set the content-type header to 'application/json'
    headers = {'content-type': 'application/json'}

    # Send the POST request
    print(f"Downloading course detail for {language}...")
    response = requests.post(url, json=payload, headers=headers)
    response_dict = response.json()

    os.makedirs('files', exist_ok=True)
    with open(os.path.join('files',f"ULHT{course}-{language}.json"), "w", encoding="utf-8") as f:
      json.dump(response_dict, f, indent=4)


    print(f"Downloading UCs for {language}...")
    for uc in response_dict['courseFlatPlan']:
      url = 'https://secure.ensinolusofona.pt/dados-publicos-academicos/resources/GetSIGESCurricularUnitDetails'

      # Define the payload data to be sent in the POST request
      payload = {
          'language': language,
          'curricularIUnitReadableCode': uc['curricularIUnitReadableCode'],
      }

      # Set the content-type header to 'application/json'
      headers = {'content-type': 'application/json'}

      # Send the POST request
      response_uc = requests.post(url, json=payload, headers=headers)

      response_uc_dict = response_uc.json()

      with open(os.path.join('files',f"{uc['curricularIUnitReadableCode']}-{language}.json"), "w", encoding="utf-8") as f:
        json.dump(response_uc_dict, f, indent=4)
