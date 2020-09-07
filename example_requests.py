import requests

req = requests.get('https://openaccess.thecvf.com/CVPR2020?day=2020-06-16')

html = req.text

header = req.headers

# If code is 200, it is correct.
status = req.status_code

print(req.ok)