import socket
from ldap3 import Server, Connection, MODIFY_REPLACE
from tkinter import messagebox as MessageBox
from tkinter import StringVar, Frame, Label, Button, Entry, Tk


class LDAPClientApp:
    def __init__(self, root):
        # Program created by: https://github.com/frkvk/
        # Any issues contact with me.
        # Here you have the variables to edit
        self.ldap_ip = 'LDAP IP'
        self.organizational_unit = 'ou=employes,dc=domain,dc=local' #Excluding the "uid=X"
        # for example with this text you have uid=user,ou=employes,dc=domain,dc=local


        self.root = root
        self.root.title("OpenLDAP_PwdChanger")
        self.root.geometry("300x260")
        self.root.resizable(0, 0)
        self.ldap_uri = f'ldap://{self.ldap_ip}'   #Change that variable before compile .exe
        self.ldaps_uri = f'ldaps://{self.ldap_ip}'
        

        self.struser = StringVar()
        self.strpass = StringVar()
        self.strnewpass = StringVar()
        
        self.frame1 = Frame(self.root, width=1200, height=600)
        self.frame1.pack()

        self.create_ui()

    def create_ui(self):
        frame_user = Label(self.frame1, text="LDAP User")
        frame_user.grid(row=0, column=0, pady=5, padx=10)

        frame_pass = Label(self.frame1, text="Password")
        frame_pass.grid(row=10, column=0, pady=5, padx=10)

        frame_newpass = Label(self.frame1, text="New Password")
        frame_newpass.grid(row=15, column=0, pady=5, padx=10)

        text_user = Entry(self.frame1, textvariable=self.struser)
        text_user.grid(row=0, column=1, pady=5, padx=10)

        text_pass = Entry(self.frame1, textvariable=self.strpass)
        text_pass.grid(row=10, column=1, pady=5, padx=10)
        text_pass.config(show="*")

        text_newpass = Entry(self.frame1, textvariable=self.strnewpass)
        text_newpass.grid(row=15, column=1, pady=5, padx=10)
        text_newpass.config(show="*")

        button_check = Button(self.frame1, text="Check Connection", command=self.verify_password)
        button_check.grid(row=50, column=1)

        self.label_check = Label(self.frame1)
        self.label_check.grid(row=52, column=1, padx=4)

        label_null1 = Label(self.frame1, text="")
        label_null1.grid(row=53, column=1, padx=4)

        label_null2 = Label(self.frame1, text=" ")
        label_null2.grid(row=80, column=1, padx=4)

        button_changepwd = Button(self.frame1, text="Change Password", command=self.change_password)
        button_changepwd.grid(row=61, column=1, padx=1)



    def starttlstry(self, user, passw, ldap_uri, port, use_ssl):
        try:
            server = Server(ldap_uri, port=port, use_ssl=use_ssl, connect_timeout=3)
            conn = Connection(server, user=f'uid={user},{self.organizational_unit}', password=f'{passw}')
            if (conn.result and conn.result['result'] != 0):
                MessageBox.showerror("Authentication Fail", f"Please check your password and try again.")
                return False
            conn.start_tls()
            if conn.bind():
                print(f"LDAP STARTTLS {port}")
                return conn
            elif conn.result['result'] == 49:
                MessageBox.showerror("Authentication Fail", f"Please check your username & password and try again.")
            else:
                print(conn.result['result'])
                return False
        except (socket.timeout, socket.error):
            pass
        except (TypeError, AttributeError):
            pass


    def create_ldap_connection(self, user, passw):
        # # START_TLS 389
        conn = self.starttlstry(user, passw, self.ldap_uri, 389, True)
        if conn: 
            return conn

        # START_TLS 636
        conn = self.starttlstry(user, passw, self.ldap_uri, 636, True)
        if conn: 
            return conn

        # # LDAPS 636
        conn = self.starttlstry(user, passw, self.ldaps_uri, 636, False)
        if conn: 
            return conn

        # # LDAP 389
        conn = self.starttlstry(user, passw, self.ldap_uri, 389, False)
        if conn: 
            return conn



    def verify_password(self):
        user = self.struser.get()
        passw = self.strpass.get()

        try:
            conn = self.create_ldap_connection(user, passw)
            if (conn and conn.bind()):
                self.label_check.config(text="Connected")
                conn.unbind()
        except socket.error as socket_err:
            error_message = str(socket_err)
            if "WinError 10061" in error_message:
                error_message = "Connection was refused by the LDAP server. Check the server's availability and configuration."
            print("Socket Error:", error_message)

        except Exception as e:
            print("Error:", e)
            self.label_check.config(text="Connection failed")
            MessageBox.showerror("Unknown Error", f"Unknown Error: \n {e} \n Please contact an Administrator.")



    def change_password(self):
        user = self.struser.get()
        passw = self.strpass.get()
        newpas = self.strnewpass.get()
        try:
            conn = self.create_ldap_connection(user, passw)
            if (conn and conn.bind()):
                result = conn.extend.standard.modify_password(f'uid={user},{self.organizational_unit}', passw, newpas)
                
                if result:
                    print("Password changed successfully")
                    MessageBox.showinfo("Password changed", "The password has been changed successfully.")
                else:
                    response = conn.result
                    print(response)
                    if "Password is in history" in response['message']:
                        MessageBox.showwarning("Error", "The new password is already in the password history.")
                    elif "Password is not being changed from existing value" in response['message']:
                        MessageBox.showwarning("Error", "The new password is the same as the current one.")
                    elif "Password fails quality checking policy" in response['message']:
                        MessageBox.showwarning("Error", "The new password does not meet complexity requirements.")
                    else:
                        print("Password could not be changed:", response['message'])
                        MessageBox.showwarning("Error", f"The password could not be changed: \n {response['message']}")
                conn.unbind()
        except socket.error as socket_err:
            error_message = str(socket_err)
            if "WinError 10061" in error_message:
                error_message = "Connection was refused by the LDAP server. Check the server's availability and configuration."
            print("Socket Error:", error_message)
        except Exception as e:
            MessageBox.showerror("Unknown Error", f"Unknown Error: \n {e} \n Please contact an Administrator.")



def main():
    raiz = Tk()
    app = LDAPClientApp(raiz)
    raiz.mainloop()

if __name__ == "__main__":
    main()

