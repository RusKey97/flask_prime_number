import requests

URL = 'http://127.0.0.1:5000'

payload = {'number': '2497345', 'operation': 'decompose', 'split_places_flag': False, 'explanatory_message': 'Да'}
payload = {'number': '2497345', 'operation': 'decompose', 'split_places_flag': True}
payload = {'number': '2497345'}
payload = {'number': '2497345', 'operation': '2497345'}
payload = {'number': 13, 'operation': 'next_prime', 'split_places_flag': True}
payload = {'number': 1, 'operation': 'prev_prime', 'split_places_flag': True}

response = requests.post(URL, headers={}, data=payload)
print(response.text)
