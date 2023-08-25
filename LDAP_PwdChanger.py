import socket
from ldap3 import Server, Connection, MODIFY_REPLACE, ALL
from tkinter import *
from tkinter import messagebox as MessageBox

class LDAPClientApp:
    def __init__(self, root):
        # Program created by: https://github.com/frkvk/
        # Any issues contact with me.
        self.root = root
        self.root.title("OpenLDAP-Client")
        self.root.geometry("300x260")
        self.root.resizable(0, 0)
        
        self.ldap_uri = 'ldap://IP:PORT'   #Change that variable before compile .exe
        
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

        label_check = Label(self.frame1)
        label_check.grid(row=52, column=1, padx=4)

        label_null1 = Label(self.frame1, text="")
        label_null1.grid(row=53, column=1, padx=4)

        label_null2 = Label(self.frame1, text=" ")
        label_null2.grid(row=80, column=1, padx=4)

        button_changepwd = Button(self.frame1, text="Cambiar Contraseña", command=self.change_password)
        button_changepwd.grid(row=61, column=1, padx=1)


    def verify_password(self):
        dn_user = f'uid={self.struser.get()},ou=employers,dc=example,dc=local' #Change that variable before compile .exe
        passw = self.strpass.get()
        server = Server(self.ldap_uri)

        conn = Connection(server, dn_user, passw)

        old_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(6)

        try:
            if conn.bind():
                self.label_check.config(text="Connected")
                conn.unbind()        
            else:
                self.label_check.config(text="Connection failed")
                MessageBox.showerror("Connection error", "Connection error with OpenLDAP")
                conn.unbind()
        except socket.timeout:
            MessageBox.showerror("Connection timeout", "Request timeout against the OpenLDAP server has elapsed.")
        except Exception as e:
            print("Error:", e)
            MessageBox.showerror("Unkown Error", f"Unkown Error,: \n {e} \n Please contact with an Administrator.")
        finally:
            socket.setdefaulttimeout(old_timeout)


    def change_password(self):
        dn_user = f'uid={self.struser.get()},ou=employers,dc=example,dc=local' #Change that variable before compile .exe
        passw = self.strpass.get()
        newpas = self.strnewpass.get()
        server = Server(self.ldap_uri, get_info=ALL)

        conn = Connection(server, dn_user, passw)
        old_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(6)

        try:
            if conn.bind():
                result = conn.extend.standard.modify_password(dn_user, passw, newpas)
                
                if result:
                    print("Password changed succesfully")
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
                        print("No se pudo cambiar la contraseña:", response['message'])
                        MessageBox.showwarning("Error", f"The password could not be changed: \n {response['message']}")
                conn.unbind()
            else:
                print("Error de autenticación")
                conn.unbind()
        except socket.timeout:
            MessageBox.showerror("Connection timeout", "Request timeout against the OpenLDAP server has elapsed.")
        except Exception as e:
            MessageBox.showerror("Unkown Error", f"Unkown Error,: \n {e} \n Please contact with an Administrator.")
        finally:
            socket.setdefaulttimeout(old_timeout)


def main():
    raiz = Tk()
    app = LDAPClientApp(raiz)
    raiz.mainloop()

if __name__ == "__main__":
    main()
