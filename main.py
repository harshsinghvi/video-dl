from urllib.request import urlopen
video_num = 1
file_num = 1
while True:
    
    link = 'https://videos-a.jwpsrv.com/content/conversions/Ux8FajpR/videos/ti073qxr-32240523.mp4-{}.ts'.format(video_num)
    response_url = urlopen(link)
    if response_url.getcode() == 200:
        file_name = 'Lecture_{}.mp4'.format(file_num) 
        print(file_name)
        with open(file_name,'wb') as f:
            f.write(response_url.read())
        video_num += 1
        file_num += 1
        print(file_num)
    else:
        print('Exited')
        break