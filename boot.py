import wifi
import ugit
import urequests
import os

wifi.wifi_setup()

stored_result = ""
if 'current_sha.txt' in os.listdir():
    try:
        f = open('current_sha.txt')
        stored_result = f.read()
        f.close()
    except OSError:
        print("sha error")


url = 'https://api.github.com/repos/cbu-egr102/esp32-public/commits/main'
headers = {
    'user-agent': 'node.js',
    'accept': 'application/vnd.github.VERSION.sha'
}
result = urequests.request('GET', url, headers=headers)
print("RESULT")
print(result.text)

try:
    f = open('current_sha.txt', 'w')
    f.write(result.text)
    f.close()
except OSError:
    print("sha error write")

if(result != stored_result):
    ugit.pull_all(isconnected=True)

#ugit.backup()
