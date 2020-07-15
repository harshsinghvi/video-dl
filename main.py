from urllib.request import urlopen
video_num = 1
file_num = 1
inp_link = input('Enter link: ')
file_pre = input('Enter File name: ')
rm=inp_link.find('mp4-')+4
rm_end=len(file_pre)
inp_link=inp_link[:rm]
# print(inp_link)

while True:
    append_str = '{}.ts'.format(video_num)
    link = inp_link + append_str
    response_url = urlopen(link)
    if response_url.getcode() == 200:
        file_post = '{}.mp4'.format(file_num) 
        file_name = 'downloads/'+file_pre + file_post
        time_escaped=video_num * 4
        print(file_name,time_escaped," seconds")

        with open(file_name,'wb') as f:
            f.write(response_url.read())
        video_num += 1
        file_num += 1
    else:
        print('Exited')
        break

# demo_link = https://videos-a.jwpsrv.com/content/conversions/Ux8FajpR/videos/kVgM3EV5-32240523.mp4-full.ts 