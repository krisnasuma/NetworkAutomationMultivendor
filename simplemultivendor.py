#import modul yang diperlukan
import paramiko #import library telnetlib
import time #jika menggunakan waktu sleep cocok digunakan pada cisco

#definisikan sebuah list untuk menampung objek SSHClient
#anggota list berisi sebuah kamus yang berisi username dan password serta info lainnya
devices = [
    {
        'ip_add' : '192.168.137.4',
        'vendor' : 'cisco',
        'username' : 'cisco',
        'password' : 'cisco'
    },
    {
        'ip_add' : '192.168.137.2',
        'vendor' : 'mikrotik',
        'username' : 'admin',
        'password' : ''
    }
]

#buat variable untuk objek SSH server serta memanggil fungsi connect
ssh_tujuan = paramiko.SSHClient()
ssh_tujuan.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#buat variable device dalam sebuah perulangan untuk mendefinisikan list yang sudah dibuat diatas
for device in devices:
    #panggil list dengan mendefinisikan variable dari list yang siap di tampung
    ssh_tujuan.connect(hostname=device['ip_add'], username=device['username'], password=device['password'])

    #tampilkan pesan berhasil koneksi
    print("Berhasil terkoneksi ke {}".format(device['ip_add']))


    #buat statement jika vendor yang terkoneksi kemungkinan cisco atau mikrotik atau bahkan keduanya 
    #jika vendor nya adalah cisco
    if device['vendor'] == 'cisco':
        config = ssh_tujuan.invoke_shell() #memanggil fungsi invoke_shell untuk menjalankan perintah pada router

        #fungsi untuk menjalankan perintah pada router cisco
        #bisa ditambahkan parameter untuk menjalankan perintah lainnya, ini hanya contoh
        config.send("conf t\n")
        config.send("int lo2\n")
        config.send("ip add 10.1.1.3 255.255.255.255\n")
        time.sleep(1) #waktu ekseskusi perintah yang ditulis di router (1 detik) agar diberikan waktu untuk perintah tersebut saat dijalankan
        #jika menggunakan paramiko wajib mensetting time sleep agar tidak terjadi error
        #sehingga command cisco bisa terkirim dengan benar

        output = config.recv(65535)  #mengambil output dari perintah yang ditulis di router
        print(output.decode()) #menampilkan output dari perintah yang ditulis di router

    #jika vendor nya adalah mikrotik
    else:

        #fungsi untuk menjalankan perintah pada router mikrotik
        #bisa ditambahkan parameter untuk menjalankan perintah lainnya, ini hanya contoh
        ssh_tujuan.exec_command("interface bridge add name loopback1\n")
        ssh_tujuan.exec_command("ip address add address=10.2.2.2/32 interface=loopback1\n")
    
    #tutup program agar berhenti tereksekusi
    ssh_tujuan.close()