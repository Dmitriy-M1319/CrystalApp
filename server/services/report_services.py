import http.client
import json
from logging import log, INFO
from typing import Tuple

from dependencies import get_settings

def get_report_by_period(date_from: str, date_to: str) -> Tuple[int, str, bytes]:
    conn = http.client.HTTPConnection(get_settings().report_server_address)
    
    data = {
        'from': date_from,
        'to': date_to
    }
    json_data = json.dumps(data)
    print(json_data)
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request('POST', "/report", body=json_data, headers=headers)
    response: http.client.HTTPResponse = conn.getresponse()

    msg = ''
    resp_data:bytes = response.read()
    if response.status != 200:
        log(INFO, f'Failed to retrieve file. Status code: {response.status}')
        response_json = json.loads(resp_data)
        msg = response_json['error']

    return response.status, msg, resp_data
