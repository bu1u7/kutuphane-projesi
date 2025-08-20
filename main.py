from Kutuphane import Kutuphane

def menu():
    print("\n--- KÜTÜPHANE MENÜSÜ ---")
    print("1. ISBN ile Kitap Ekle")
    print("2. Kitap Sil")
    print("3. Kitapları Listele")
    print("4. Kitap Ara")
    print("5. Çıkış")

def main():
    kutuphane = Kutuphane()
    while True:
        menu()
        secim = input("Seçiminiz: ")

        if secim == "1":
            isbn = input("ISBN: ")
            if kutuphane.add_book_by_isbn(isbn):
                print("Kitap başarıyla eklendi.")
            else:
                print("Kitap eklenemedi veya zaten kayıtlı!")

        elif secim == "2":
            isbn = input("Silinecek kitabın ISBN numarası: ")
            if kutuphane.remove_book(isbn):
                print("Kitap başarıyla silindi.")
            else:
                print("Kitap bulunamadı!")

        elif secim == "3":
            kitaplar = kutuphane.list_books()
            if not kitaplar:
                print("Kütüphane boş.")
            else:
                print("\n--- Kütüphanedeki Kitaplar ---")
                for k in kitaplar:
                    print(k)

        elif secim == "4":
            isbn = input("Aranacak ISBN: ")
            kitap = kutuphane.find_book(isbn)
            if kitap:
                print("Bulundu:", kitap)
            else:
                print("Kitap bulunamadı.")

        elif secim == "5":
            print("Programdan çıkılıyor...")
            break
        else:
            print("Geçersiz seçim!")

if __name__ == "__main__":
    main()
