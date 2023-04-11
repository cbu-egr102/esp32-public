import wifi
import ugit
import urequests
import os

wifi.wifi_setup()

stored_result = ""
if 'current_sha.txt' in os.listdir():
    try:
        print("Getting current SHA")
        f = open('current_sha.txt')
        stored_result = f.read()
        f.close()
    except OSError:
        print("sha error")

print("Getting latest SHA")
url = 'https://api.github.com/repos/cbu-egr102/esp32-public/commits/main'
headers = {
    'user-agent': 'node.js',
    'accept': 'application/vnd.github.VERSION.sha'
}
result = urequests.request('GET', url, headers=headers)
print("SHA RESULT")
print(result.text)

print("Writing latest SHA")
try:
    f = open('current_sha.txt', 'w')
    f.write(result.text)
    f.close()
except OSError:
    print("sha error write")

if(stored_result == ""):
    stored_result = result.text

if(result.text != stored_result):
    print("Pulling from repo")
    ugit.pull_all(isconnected=True)

#ugit.backup()
