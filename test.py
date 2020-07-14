import requests 
base_url="https://videos-a.jwpsrv.com/content/conversions/Ux8FajpR/videos/"
resource_id="ti073qxr-32240523.mp4-"
append=".ts"

i=2
while True: 
    resource= base_url + resource_id + str(i) + append
    response = requests.get(resource)
    print( i, " => ", response.status_code)
    i = i +1 