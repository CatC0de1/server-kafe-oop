from abc import ABC, abstractmethod
import time
import os

class MenuItem(ABC):
    def __init__(self, nama, harga):
        self.nama = nama
        self.harga = harga

    @abstractmethod
    def tampilkan_info(self):
        pass


class Makanan(MenuItem):
    def __init__(self, nama, harga):
        super().__init__(nama, harga)

    # override dari method tampilkan_info di Class MenuItem(ABC)
    def tampilkan_info(self):
        print(f"Makanan: {self.nama} - Rp {self.harga}")


class Minuman(MenuItem):
    def __init__(self, nama, harga):
        super().__init__(nama, harga)

    # override dari method tampilkan_info di Class MenuItem(ABC)
    def tampilkan_info(self):
        print(f"Minuman: {self.nama} - Rp {self.harga}")


class Kafe():
    def __init__(self, nama_kafe):
        self.nama_kafe = nama_kafe
        self.makanan = [
            Makanan("Nasi Goreng", 15000), Makanan("Mie Goreng", 12000),
            Makanan("Ayam Bakar", 25000), Makanan("Soto Ayam", 15000),
            Makanan("Bakso", 10000)
        ]
        self.minuman = [
            Minuman("Air Putih Kemasan", 5000), Minuman("Es Teh", 8000),
            Minuman("Teh Hangat", 6000), Minuman("Es Kopi", 8000),
            Minuman("Kopi Hangat", 6000), Minuman("Es Jeruk", 8000),
            Minuman("Jeruk Hangat", 6000), Minuman("Es Milo", 8000),
            Minuman("Es Campur", 12000)
        ]
        self.pesanan = []
        self.total_harga_sebelum_diskon = 0

    def tampilkan_menu(self):
        self.pesanan = []
        self.total_harga_sebelum_diskon = 0
        print(f"Selamat datang di {self.nama_kafe}\n")
        print("                                           PROMO SPESIAL!!!        ")
        print("   1. Dapatkan diskon sebesar 20% dengan pembelian 3 porsi Nasi Goreng dan 2 porsi Mie Goreng")
        print("   2. Dapatkan diskon sebesar 10% dengan pembelian Paket Bakso, terdiri dari 1 porsi Bakso dan 1 gelas Es Teh")
        print("   3. Dapatkan Es Teh secara gratis dengan pembelian 2 porsi Ayam Bakar (Pastikan menambahkan Es Teh ke dalam keranjang)\n")

        print("Menu Pilihan Makanan:")
        for i, item in enumerate(self.makanan, 1):
            print(f"       {i}. {item.nama} - Rp {item.harga}")
        print("Menu Pilihan Minuman:")
        for i, item in enumerate(self.minuman, len(self.makanan) + 1):
            print(f"       {i}. {item.nama} - Rp {item.harga}")
        print("       15. Selesai Memesan")

    # overloading dalam method tambah_pesanan dimana perbedaan nya ada pada parameter jumlah
    def tambah_pesanan(self, pilihan, jumlah=1):
        total_menu = len(self.makanan) + len(self.minuman)
        if 1 <= pilihan <= total_menu:
            if pilihan <= len(self.makanan):
                item_dipilih = self.makanan[pilihan - 1]
            else:
                item_dipilih = self.minuman[pilihan - len(self.makanan) - 1]
            
            for _ in range(jumlah):
                self.pesanan.append(item_dipilih)
                self.total_harga_sebelum_diskon += item_dipilih.harga
            print(f"{jumlah} pesanan '{item_dipilih.nama}' ditambahkan ke keranjang.")

            print("Mau memesan makanan / minuman lagi? (Tekan 15 jika selesai memesan)\n")

    def tampilkan_pesanan(self):
        print("Pesanan Anda:")
        for i, item in enumerate(self.pesanan, 1):
            print(f"{i}. {item.nama} - Rp. {item.harga}")

    def hitung_total(self):
        return sum(item.harga for item in self.pesanan)

    # implementasi metode cek_diskon dari DiskonInterface
    def cek_diskon(self):
        total_harga = self.hitung_total()

        if sum(1 for item in self.pesanan if item.nama == "Nasi Goreng") >= 3 and \
           sum(1 for item in self.pesanan if item.nama == "Mie Goreng") >= 2:
            diskon = 0.2 * (self.makanan[0].harga * 3 + self.makanan[1].harga * 2)
            total_harga -= int(diskon)
            print("Anda mendapatkan diskon 20% untuk 3 Nasi Goreng dan 2 Mie Goreng!")

        if sum(1 for item in self.pesanan if item.nama == "Bakso") >= 1 and \
           sum(1 for item in self.pesanan if item.nama == "Es Teh") >= 1:
            diskon = 0.1 * (self.makanan[4].harga + self.minuman[1].harga)
            total_harga -= int(diskon)
            print("Anda mendapatkan diskon 10% untuk Paket Bakso!")

        if sum(1 for item in self.pesanan if item.nama == "Ayam Bakar") >= 2 and \
           sum(1 for item in self.pesanan if item.nama == "Es Teh") >= 1:
            es_teh_harga = self.minuman[1].harga
            total_harga -= es_teh_harga
            print("Anda mendapatkan Es Teh gratis!")

        return total_harga

    def jalankan(self):
        self.tampilkan_menu()
        while True:
            print("Pilih menu (1-15): ", end='')
            pilihan = int(input())
            print()

            if pilihan == 15:
                self.tampilkan_pesanan()
                total_harga = self.cek_diskon()
                print(f"Total Harga: Rp {total_harga}\n")
                input('Tekan enter untuk keluar.')
                os.system('cls')
                self.tampilkan_menu()
            elif pilihan == 0 or pilihan > 15:
                print("Pilihan tidak valid!")
                time.sleep(2)
                os.system('cls')
                self.tampilkan_menu() 
            else:
                pilihanJumlah = str(input("Memesan lebih dari satu(y/n)?: "))
                if pilihanJumlah.lower() == "y":
                    jumlah = int(input("Masukkan jumlah pesanan: "))
                    self.tambah_pesanan(pilihan, jumlah)
                else:
                    self.tambah_pesanan(pilihan)


kafe = Kafe("Lha Iki Kafe")
kafe.jalankan()