This code updates 'USER111'  'USER112' for the list of sites provided, exactly in the pattern under the shinken_resources tag
    a. USER111 – This is a username (Default User : IDM_user)
    b. USER112 – This is a password (Default syntax for the password : <SITEID>$n1mD@1P@D19 )

Example – For site BAK00 , the username is IDM_user and password is BAK00$n1mD@1P@D19. Then the updated value of USER111 and USER112 will be –
USER111: "{+gAAAAABdchtFRjCKEgJ7IWCleY--WfeY2Gpa-3GCmeBvJZrD-yE6r3XPyI9gA16PUnL8xGgOC1JBPolHWBiu3kKYgusg_jbd9w==+}"
USER112: "{+gAAAAABdchvkvoRJP_J52QXTzwR2q8t0UkRNp7Hbg0JOLadxh3Kyr22jJrxAvq1Gi3V1lswJlL1759xTfgSgmXtWiUAB8-D3mHBzo3bRHOG6WG1r23Epu8Q=+}"

Instructions before running the file:
1. Please provide the list of sites (in capital letters) in a seperate file with each Site in a New Line
2. Code automatically updates the corresponding site in smaller case. (No need to give smaller case site names) 
3. Update the correct 'SVN_URL', 'SVN_USERNAME' , 'SVN_PASSWORD'(line 13,14,15 in the code) based on the environment of SVN

Instructions to run file :
1. Open a terminal / command prompt provide the sites_list file as the 2nd argument as shown in below example
    Format : python <<updated.py>> <<sites_list_file>>
    Example:  python SVNupdater_for_user111_and_112_v3.py sites.txt
2. Encrypted strings will be in single quote in lhost.yml if "SVNupdater_for_user111_and_112_v3.py" file is used.
   Encrypted strings will be in double quote in lhost.yml if "SVNupdater_for_user111_and_112_v3_doublequote.py" file is used.

In case one or more Sites have failed to update , a list of failed sites will be shown in at the end.
A log file will be created with all changes made for each day any changes are made in the same folder of files.
Name of log file will be in "svn_changes-<month>-<day>-<year>.log" format.

