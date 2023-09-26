# OpenLDAP_PwdChanger
A program to let users change the OpenLDAP password inside our organization

The purpose of this program is to create an .exe to provide members of our organization with the ability to regularly change their LDAP passwords.
It's important to know that this program works with OpenLDAP's ppolicy, adhering to the complexity requirements set by the server, historical checks, and passwords stored in SSHA format.

Currently, the program only allows insecure LDAP connections, and support for LDAPS will be added in the near future. It is recommended to use the program externally with a VPN or within a trusted network.

The program can be compiled into an .exe file with included dependencies, but prior to this, it's necessary to modify lines 15, 64, and 91 (LDAP variables).

The steps to create an .exe are as follows:

    Have Python installed on your system.
    Have PyInstaller installed and its path configured.
    Open a cmd terminal.

First, open a cmd terminal with administrator privileges and execute the following commands (if you want to add an icon to the program):
- pyinstaller --add-data "icon.ico;dist\icon.ico" -i "icon.ico" LDAP_PwdChanger.py
- pyinstaller -F -w -i "icon.ico" LDAP_PwdChanger.py

If you dont want to have an icon in the program:
- pyinstaller LDAP_PwdChanger.py
- pyinstaller -F -w LDAP_PwdChanger.py
  
Finally, within the "Dist" folder, there will be an .exe file that can be distributed to users. You can delete the remaining folders and keep the .py and .exe files.

Preview:

If you have problem with the antivirus, u need to follow this manual:
https://plainenglish.io/blog/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184#7-re-build-your-exe-with-pyinstaller-and-make-sure-its-not-being-be-flagged-as-a-virus
In the step 6.3 if you have python installed from the windows app store, u need to run:
- pip install .

![imagen](https://github.com/frkvk/OpenLDAP_PwdChanger/assets/117442111/ac0f560e-c206-42e7-be89-3e393223f0ff)


