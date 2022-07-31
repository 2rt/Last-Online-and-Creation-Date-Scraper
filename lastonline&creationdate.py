import ctypes, requests
from threading import Thread

threadc = 100

usernames = open('usernames.txt','r',errors='ignore').read().splitlines()
total = len(usernames)
s = requests.session()
proxy = set()

with open("proxies.txt", "r") as f:
    file_lines1 = f.readlines()
    for line1 in file_lines1:
        proxy.add(line1.strip())
        
proxies = {
    'http': 'http://'+random.choice(list(proxy))
}


r = requests.get('http://www.roblox.com/',proxies=proxies)
done = 0
output = []

def thread():
    global done
    while usernames:
        username = usernames.pop(0)
        try:
            r = requests.get(f'https://www.roblox.com/user.aspx?username={username}').url
            if 'www.roblox.com/users/' in r:
                userid = r.split('/')[-2]
                created = requests.get(f'https://users.roblox.com/v1/users/{userid}/').json()['created'].split('-')[0]
                lastonline = requests.get(f'https://api.roblox.com/users/{userid}/onlinestatus/').json()['LastOnline'].split('-')[0]
                output.append(f'{lastonline}:{created}:{username}\n')
            done += 1
        except:
            usernames.append(username)

print(f'Starting {threadc} threads.')
for i in range(threadc):
    Thread(target=thread).start()

while 1:
    finished = done
    ctypes.windll.kernel32.SetConsoleTitleW(f'Last Online Scraper | Done: {finished}/{total}')
    if finished == total: break

with open('out.txt','w',errors='ignore') as f:
    f.writelines(output)

input('Finished.')
