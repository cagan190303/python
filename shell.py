import os
import sys
import subprocess
import shutil

def py_editor():
    print("py_editor açılıyor...")
    print("py_editor açıldı")
    code_lines = []
    while True:
        line = input("py_editor > ")
        if line.strip() == "editor.exit":
            print("Editörden çıkılıyor...")
            break
        elif line.strip() == "program.fnish":
            print("Kod yazımı tamamlandı, ancak editör açık kalıyor.")
            break
        else:
            code_lines.append(line)
    return code_lines

def save_program(code_lines, storage_path, filename):
    if not code_lines:
        print("Hata: Kaydedilecek kod bulunmuyor.")
        return

    filepath = os.path.join(storage_path, filename)
    # Dosya yazma işleminde UTF-8 kodlaması kullanılıyor
    with open(filepath, "w", encoding="utf-8") as f:
        for line in code_lines:
            f.write(line + "\n")
    print(f"Program kaydedildi: {filepath}")
    return filepath

def run_program(filepath):
    if not os.path.exists(filepath):
        print("Hata: Program dosyası bulunamadı.")
        return
    # Sadece .py uzantılı dosyalar çalıştırılabilir
    if not filepath.endswith(".py"):
        print("Hata: Sadece .py dosyaları çalıştırılabilir.")
        return

    print("Program başlatılıyor...\n")
    subprocess.run([sys.executable, filepath])  # Burada .py dosyasını çalıştırıyoruz
    print("\nProgram bitti. Kod içeriği:")
    with open(filepath, "r", encoding="utf-8") as f:  # UTF-8 kodlaması ile dosyayı okuyoruz
        print(f.read())

def write_to_code(code_lines, storage_path):
    print("Kod ekleme moduna girildi. Çıkmak için 'editor.exit' yazın.")
    while True:
        line = input("yaz > ")
        if line.strip() == "editor.exit":
            print("Kod ekleme tamamlandı. Kaydediliyor...")
            # Dosya adını ve uzantısını soruyoruz
            filename = input("Dosya adını ve uzantısını girin (örneğin, 'dosya.txt'): ").strip()
            if not filename:
                print("Hata: Geçerli bir dosya adı girin.")
                continue
            save_program(code_lines, storage_path, filename)
            break
        code_lines.append(line)

def edit_code(code_lines, storage_path):
    try:
        print("Tüm içeriği mi silmek istiyorsunuz, yoksa üzerine mi eklemek istiyorsunuz?")
        action = input("Tüm içeriği silmek için 's', üzerine eklemek için 'e' girin: ").strip().lower()
        if action == "s":
            print("Kod tamamen silinecek. Yeni içeriği girin. Bitirmek için 'editor.exit' yazın.")
            code_lines.clear()
            while True:
                line = input("yeni > ")
                if line.strip() == "editor.exit":
                    print("Yeni içerik ekleme tamamlandı.")
                    # Dosya adını ve uzantısını soruyoruz
                    filename = input("Dosya adını ve uzantısını girin (örneğin, 'dosya.txt'): ").strip()
                    if not filename:
                        print("Hata: Geçerli bir dosya adı girin.")
                        continue
                    save_program(code_lines, storage_path, filename)
                    break
                code_lines.append(line)
        elif action == "e":
            print("Mevcut içeriğe ekleme yapılıyor. Bitirmek için 'editor.exit' yazın.")
            while True:
                line = input("ekle > ")
                if line.strip() == "editor.exit":
                    print("Ekleme tamamlandı.")
                    # Dosya adını ve uzantısını soruyoruz
                    filename = input("Dosya adını ve uzantısını girin (örneğin, 'dosya.txt'): ").strip()
                    if not filename:
                        print("Hata: Geçerli bir dosya adı girin.")
                        continue
                    save_program(code_lines, storage_path, filename)
                    break
                code_lines.append(line)
        else:
            print("Geçersiz seçenek. 's' tüm içeriği silmek için, 'e' üzerine eklemek için kullanılır.")
    except ValueError:
        print("Hata: Lütfen geçerli bir giriş yapın.")

def delete_code(storage_path):
    # 1. Dosya adı ve uzantısını kullanıcıdan alıyoruz
    filename = input("Silmek istediğiniz dosyanın adını ve uzantısını girin (örneğin, 'dosya.txt'): ").strip()

    # 2. Dosya yolu oluşturuyoruz
    filepath = os.path.join(storage_path, filename)

    # 3. Dosyanın varlığını kontrol ediyoruz
    if not os.path.exists(filepath):
        print(f"Hata: '{filename}' dosyası bulunamadı.")
        return

    # 4. Dosyayı silme işlemi
    os.remove(filepath)
    print(f"'{filename}' dosyası silindi.")

def read_code(storage_path):
    # 1. Dosya adı ve uzantısını kullanıcıdan alıyoruz
    filename = input("Okumak istediğiniz dosyanın adını ve uzantısını girin (örneğin, 'dosya.txt'): ").strip()

    # 2. Dosya yolu oluşturuyoruz
    filepath = os.path.join(storage_path, filename)

    # 3. Dosyanın varlığını kontrol ediyoruz
    if not os.path.exists(filepath):
        print(f"Hata: '{filename}' dosyası bulunamadı.")
        return

    # 4. Dosyayı okuma işlemi
    print(f"'{filename}' dosyasının içeriği:")
    with open(filepath, "r", encoding="utf-8") as f:  # UTF-8 kodlaması ile dosyayı okuyoruz
        print(f.read())  # Dosyanın içeriğini yazdırıyoruz

# Bilgisayardaki sürücüleri listeleme
def list_drives():
    if sys.platform == "win32":  # Windows sistem
        print("Windows Sürücüleri:")
        drives = [drive for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{drive}:\\")]
        for drive in drives:
            print(f"{drive}:\\")
    elif sys.platform == "darwin" or sys.platform == "linux":  # Unix tabanlı sistemler (Mac/Linux)
        print("Disk Sürücüleri:")
        result = subprocess.run(["df", "-h"], stdout=subprocess.PIPE, text=True)
        print(result.stdout)

# Storage dizini ve alan kullanımını gösterme
def show_storage_usage(storage_path):
    if not os.path.exists(storage_path):
        print(f"Error: {storage_path} does not exist.")
        return
    
    total, used, free = shutil.disk_usage(storage_path)
    print(f"Storage Usage for {storage_path}:")
    print(f"Total: {total // (2**30)} GB")
    print(f"Used: {used // (2**30)} GB")
    print(f"Free: {free // (2**30)} GB")

def main():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../rm-os/storage"))
    if not os.path.exists(base_path):
        os.makedirs(base_path)  # storage klasörü yoksa oluştur
    
    code_lines = []
    current_project = ""
    saved_file = None

    print("RM-OS - Depolama Yolu: " + base_path)

    while True:
        command = input(f"{base_path} > ").strip()
        parts = command.split(" ", 1)
        cmd = parts[0].lower()

        try:
            if cmd == "exit":
                print("RM'den çıkılıyor...")
                sys.exit(0)
            elif cmd == "py":
                filename = input("Çalıştırmak istediğiniz Python dosyasının adını ve uzantısını girin (örneğin, 'dosya.py'): ").strip()
                filepath = os.path.join(base_path, filename)
                run_program(filepath)  # Kaydedilen dosya çalıştırılır
            elif cmd == "write":
                write_to_code(code_lines, base_path)
            elif cmd == "edit":
                edit_code(code_lines, base_path)
            elif cmd == "delete":
                delete_code(base_path)  # Dosya silme işlemi için storage_path'i parametre olarak geçiyoruz
            elif cmd == "read":
                read_code(base_path)  # Dosya okumak için storage_path'i parametre olarak geçiyoruz
            elif cmd == "disc":
                list_drives()  # Sürücüleri listele
            elif cmd == "storage":
                show_storage_usage(base_path)  # Storage alanını göster
            else:
                print("Geçersiz komut veya eksik parametre. Desteklenen komutlar: py, write, edit, delete, read, disc, storage, exit")
        except Exception as e:
            print(f"Hata: {e}")

if __name__ == "__main__":
    main()
