import base64, getpass, socket, ssl, sys

# Global variables
mailserv = ''
mailport = -1
mailfrom = ''
mailrcpt = ''
mailmess = ''
username = ''
password = ''
cryptmethod = 'none'


# Function - getServerAddr
# Deskripsi - Menyuruh user untuk memasukkan alamat mail server
def getServAddr():
    global mailserv
    mailserv = input('Masukkan alamat  mail server: ')

# Function - getServerPort
# Deskripsi - Menyuruh user untuk memasukkan nomor port server
def getServPort():
    global mailport
    while True:
        p = int(input('Masukkan alamat port untuk terhubung: '))
        if not (p < 0 or p > 65535):
            mailport = p
            return
        else:
            print('Invalid input. nomor port harus diantara 0 sampai 65,535.')

# Function - getFromAddr
# Deskripsi - Menyuruh user untuk memasukkan email pengirim
def getFromAddr():
    global mailfrom
    mailfrom = input('Masukkan alamat Email Pengirim: ')

# Function - getRcptAddr
# Description - Menyuruh user untuk memasukkan  email tujuan
def getRcptAddr():
    global mailrcpt
    mailrcpt = input('Masukkan alamat email tujuan: ')

# Function - getMailMsg
# Description - Menyuruh user untuk memasukkan pesan. Gunakan ctrl+z  lalu enter untuk mengirim
def getMailMess():
    global mailmess
    print('--------------------------------------------------------------------------------')
    print('|        Masukkan Pesan Anda. Kirim dengan ctrl+z dan tekan enter(EOF).        |')
    print('--------------------------------------------------------------------------------')
    mailmess = sys.stdin.read(-1)

# Function - getUserName
# Deskripsi - Menyuruh pengguna untuk memasukkan user(email) untuk autentikasi
def getUserName():
    global username
    username = input('Masukkan username(email) anda: ')

# Function - getPassword
# Deskripsi - Menyuruh pengguna untuk memasukkan password to autentikasi
def getPassword():
    global password
    password = getpass.getpass('Masukkan password anda: ')

# Function - getCryptoOpt
# Description - asks the user to select their method of encryption
def getCryptoOpt():
    global cryptmethod
    while True:
        c = input('Choose an encryption protocol (TLS, SSL, or none): ')
        if (c == 'TLS') or (c == 'SSL') or (c == 'none'):
            cryptmethod = c
            return
        else:
            print("Invalid choice!")
        

# Function - dispMenu
# Description - Menampilkan menu Utama
def dispMenu():
    print("--------------------------------------------------------------------------------")
    print("| Welcome to Python Mailer! | ** | Edit parameters dibawah dan tekan send!      |")
    print("--------------------------------------------------------------------------------")
    print("1) SMTP Server: " + mailserv)
    if mailport == -1:
        print("2) Port: ")
    else:
        print("2) Port: " + str(mailport))
    print("3) From: " + mailfrom)
    print("4) To: " + mailrcpt)
    print("5) Username: " + username)
    print("6) Password: <not displayed>")
    print("7) Crypto: " + cryptmethod)

# Function - mainLoop
# Deskripsi - menghandle mainloop pada program
def mainLoop():
    useropt = 'derp'
    while useropt != 'send':
        dispMenu()
        useropt = input()
        if useropt == '1':
            getServAddr()
        elif useropt == '2':
            getServPort()
        elif useropt == '3':
            getFromAddr()
        elif useropt == '4':
            getRcptAddr()
        elif useropt == '5':
            getUserName()
        elif useropt == '6':
            getPassword()
        elif useropt == '7':
            getCryptoOpt()
        elif useropt == 'send':
            getMailMess()
            smtpSession()
        else:
            print('Invalid input. Silahkan Masuk Kembali.')

# Function - getSSLSocket
# Deskripsi - menambahkan soket baru, membungkusnya ke SSL context, dan melakukan "return"
def getSSLSocket():
    return ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), ssl_version=ssl.PROTOCOL_SSLv23)

# Function - getTLSSocket
# Deskripsi - menambahkan soket baru, membungkusnya ke TLS context, dan melakukan "return" 
def getTLSSocket():
    return ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), ssl_version=ssl.PROTOCOL_TLSv1)

# Function - getPlainSocket
# Deskripsi - menambahkan plain socket baru and melakukan return 
def getPlainSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Function - smtpSession
# Deskripsi - menghandle pengiriman pesan
def smtpSession():
    # Get the socket
    if cryptmethod == 'SSL':
        sock = getSSLSocket()
    elif cryptmethod == 'TLS':
        sock = getTLSSocket()
    else:
        sock = getPlainSocket()
    # Melakukan percobaan  untuk koneksi ke  SMTP server
    sock.connect((mailserv, mailport))
    # Menerima respon dari server dan memprint 
    respon = sock.recv(2048)
    print(str(respon, 'utf-8'))
    # Memprint Respon
    heloMesg = 'HELO Dirga\r\n'
    print(heloMesg)
    sock.send(heloMesg.encode('utf-8'))
    respon = sock.recv(2048)
    print(str(respon, 'utf-8'))
    # Autentikasi terhadap Server
    authMesg = 'AUTH LOGIN\r\n'
    crlfMesg = '\r\n'
    print(authMesg)
    sock.send(authMesg.encode('utf-8'))
    respon = sock.recv(2048)
    print(str(respon, 'utf-8'))
    user64 = base64.b64encode(username.encode('utf-8'))
    pass64 = base64.b64encode(password.encode('utf-8'))
    print(user64)
    sock.send(user64)
    sock.send(crlfMesg.encode('utf-8'))
    respon = sock.recv(2048)
    print(str(respon, 'utf-8'))
    print(pass64)
    sock.send(pass64)
    sock.send(crlfMesg.encode('utf-8'))
    respon = sock.recv(2048)
    print(str(respon, 'utf-8'))
    # Memberitahu server tentang pengirim pesan
    fromMesg = 'MAIL FROM: <' + mailfrom + '>\r\n'
    print(fromMesg)
    sock.send(fromMesg.encode('utf-8'))
    respon = sock.recv(2048)
    print(str(respon, 'utf-8'))
    # memberitahu server tentang penerima pesan
    rcptMesg = 'RCPT TO: <' + mailrcpt + '>\r\n'
    print(rcptMesg)
    sock.send(rcptMesg.encode('utf-8'))
    respon = sock.recv(2048)
    print(str(respon, 'utf-8'))
    # Memberikan ke server mengenai pesan
    dataMesg = 'DATA\r\n'
    print(dataMesg)
    sock.send(dataMesg.encode('utf-8'))
    respon = sock.recv(2048)
    print(str(respon, 'utf-8'))
    mailbody = mailmess + '\r\n'
    print(mailbody)
    sock.send(mailbody.encode('utf-8'))
    fullStop = '\r\n.\r\n'
    print(fullStop)
    sock.send(fullStop.encode('utf-8'))
    respon = sock.recv(2048)
    print(str(respon, 'utf-8'))
    # Signal server untuk keluar
    quitMesg = 'QUIT\r\n'
    print(quitMesg)
    sock.send(quitMesg.encode('utf-8'))
    respon = sock.recv(2048)
    print(str(respon, 'utf-8'))
    # Tutup socket jika selesai
    sock.close()

mainLoop()