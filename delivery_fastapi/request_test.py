import requests

headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzY0NzgyMDAxfQ.NZXsxf4Sr2dEijA3Zqoj0V0MCWokkqjjIjpXtW-exn8'
}

response = requests.get('http://127.0.0.1:8000/auth/refresh', headers=headers)

print(f'Status: {response.status_code}')
print(f'Headers: {response.headers}')
print(f'JSON: {response.json()}')
