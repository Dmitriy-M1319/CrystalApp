import http.client
import json

from dependencies import get_settings

def get_report_by_period(date_from: str, date_to: str, filepath: str):
    conn = http.client.HTTPConnection(get_settings().report_server_address)
    
    data = {
        'from': date_from,
        'to': date_to
    }
    json_data = json.dumps(data)
    
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request('POST', "/report", body=json_data, headers=headers)
    response = conn.getresponse()

    if response.status == 200:
        file_data = response.read()
        with open(filepath, 'wb') as file:
            file.write(file_data)
        print(f'File saved to {filepath}')
    else:
        print(f'Failed to retrieve file. Status code: {response.status}')

    return
