import requests


lhost_url = 'http://161.85.111.157/svn/ibc/sites/ARJUN/lhost.yml'
r = requests.get(lhost_url, auth=('operator', 'st3nt0r'))
with open('C:\\Users\\320073408\\OneDrive - Philips\\Documents\\Philips Documents\\SVNUpdater_Script\\Arjun_Lhost_2.yml', 'w') as f:
    f.write(r.content)
