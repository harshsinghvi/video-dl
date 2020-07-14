from urllib.request import urlopen
video_num = 1
file_num = 1
inp_link = input()
while True:
    
    append_str = '{}.ts'.format(video_num)
    link = inp_link + append_str
    response_url = urlopen(link)
    if response_url.getcode() == 200:
        file_name = 'Lecture_{}.mp4'.format(file_num) 
        with open(file_name,'wb') as f:
            f.write(response_url.read())
        video_num += 1
        file_num += 1
    else:
        print('Exited')
        break