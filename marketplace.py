import csv
from collections import deque
from datetime import datetime

# ========== STRUKTUR DATA UAS ==========
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def tambah_depan(self, data):
        node = Node(data)
        node.next = self.head
        self.head = node

    def hapus(self, kode):
        curr = self.head
        prev = None
        while curr:
            if curr.data['kode_produk'] == kode:
                if prev: prev.next = curr.next
                else: self.head = curr.next
                return curr.data
            prev, curr = curr, curr.next
        return None

    def cari(self, kode):
        curr = self.head
        while curr:
            if curr.data['kode_produk'] == kode:
                return curr.data
            curr = curr.next
        return None

    def update(self, kode, data_baru):
        curr = self.head
        while curr:
            if curr.data['kode_produk'] == kode:
                curr.data.update(data_baru)
                return True
            curr = curr.next
        return False

    def semua_data(self):
        data = []
        curr = self.head
        while curr:
            data.append(curr.data)
            curr = curr.next
        return data

# ========== GLOBAL ==========
db = LinkedList() # Linked List
hash_db = {} # Hash Map buat search O(1)
undo_stack = [] # Stack buat undo
checkout_queue = deque() # Queue antrian bayar
preorder_queue = deque() # Queue preorder
sku_stack = {} # Stack buat generate SKU
kategori = {}
FILE_PRODUK = 'produk.csv'

# ========== FILE CSV ==========
def load_kategori():
    try:
        with open('kategori_makeup.csv', 'r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                row['kapasitas_gudang'] = int(row['kapasitas_gudang'])
                row['harga_modal'] = int(row['harga_modal'])
                row['terdaftar'] = int(row['terdaftar'])
                kategori[row['nama_kategori']] = row
        print(f"✓ Kategori: {len(kategori)} jenis dimuat")
    except FileNotFoundError:
        print("✗ bikin kategori_makeup.csv dulu!")

def simpan_kategori():
    with open('kategori_makeup.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=kategori[list(kategori.keys())[0]].keys())
        writer.writeheader()
        writer.writerows(kategori.values())

def simpan_produk():
    with open(FILE_PRODUK, 'w', newline='', encoding='utf-8') as f:
        field = ['kode_produk','nama_produk','stok','kategori','harga_jual','no_supplier','status','stok_masuk','sku']
        writer = csv.DictWriter(f, fieldnames=field)
        writer.writeheader()
        writer.writerows(db.semua_data())

def load_produk():
    try:
        with open(FILE_PRODUK, 'r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                row['stok'] = int(row['stok'])
                row['harga_jual'] = int(row['harga_jual'])
                db.tambah_depan(row)
                hash_db[row['kode_produk']] = row # Hash Map
                kat = row['kategori']
                if kat not in sku_stack: sku_stack[kat] = []
                sku_stack[kat].append(row['sku'])
                if row['stok'] > 0: checkout_queue.append(row['kode_produk'])
                else: preorder_queue.append(row['kode_produk'])
        print(f"✓ Produk: {len(hash_db)} item dimuat")
    except FileNotFoundError:
        print("! produk.csv kosong, akan dibuat otomatis")

# ========== FITUR CRUD ==========
def create_produk():
    print("\n=== TAMBAH PRODUK ===")
    while True:
        kode = input("Kode Produk: ").upper().strip()
        if len(kode) < 3: print("Min 3 karakter!")
        elif kode in hash_db: print("Kode udah ada!")
        else: break

    nama = input("Nama Produk: ").strip()
    while not nama: nama = input("Nama: ").strip()

    stok = int(input("Stok: "))
    kat = input(f"Kategori {list(kategori.keys())}: ").upper()
    while kat not in kategori: kat = input("Kategori salah! Ulang: ").upper()

    harga = int(input("Harga Jual Rp: "))
    supplier = input("No Supplier 08...: ")
    while not supplier.startswith('08'): supplier = input("Harus 08...: ")

    # Auto generate
    status = "Tersedia" if stok > 0 else "Preorder"
    sku = generate_sku(kat)
    tanggal = datetime.now().strftime('%Y-%m-%d')

    data = {
        'kode_produk': kode, 'nama_produk': nama, 'stok': stok,
        'kategori': kat, 'harga_jual': harga, 'no_supplier': supplier,
        'status': status, 'stok_masuk': tanggal, 'sku': sku
    }

    db.tambah_depan(data)
    hash_db = data # Hash Map
    undo_stack.append({'aksi':'tambah', 'data':data})

    if stok > 0: checkout_queue.append(kode)
    else:
        preorder_queue.append(kode)
        kategori[kat]['terdaftar'] += 1
        simpan_kategori()

    simpan_produk()
    print(f"✓ Berhasil! SKU: {sku} | Status: {status}")

def read_produk():
    print("\n=== CARI PRODUK ===")
    kode = input("Input Kode: ").upper()
    if kode in hash_db:
        p = hash_db
        print("\n--- Detail ---")
        for k,v in p.items(): print(f"{k:12}: {v}")
    else:
        print("✗ Produk tidak ditemukan!")

def update_produk():
    print("\n=== UPDATE PRODUK ===")
    kode = input("Kode yg mau diupdate: ").upper()
    if kode not in hash_db:
        print("✗ Kode tidak ada!")
        return

    p = hash_db
    print(f"Lama: {p['nama_produk']} | Stok: {p['stok']} | Harga: {p['harga_jual']}")

    nama = input("Nama baru [Enter=skip]: ").strip()
    stok = input("Stok baru [Enter=skip]: ").strip()
    harga = input("Harga baru [Enter=skip]: ").strip()

    update = {}
    if nama: update['nama_produk'] = nama
    if stok:
        stok = int(stok)
        update['stok'] = stok
        update['status'] = "Tersedia" if stok > 0 else "Preorder"
    if harga: update['harga_jual'] = int(harga)

    if update:
        undo_stack.append({'aksi':'update', 'kode':kode, 'lama':p.copy()})
        db.update(kode, update)
        hash_db.update(update)
        simpan_produk()
        print("✓ Update berhasil!")
    else:
        print("Tidak ada perubahan")

def delete_produk():
    print("\n=== HAPUS PRODUK ===")
    kode = input("Kode yg mau dihapus: ").upper()
    if kode not in hash_db:
        print("✗ Kode tidak ada!")
        return

    if input(f"Hapus {hash_db['nama_produk']}? y/n: ").lower() == 'y':
        data_hapus = db.hapus(kode)
        del hash_db
        undo_stack.append({'aksi':'hapus', 'data':data_hapus})
        if kode in checkout_queue: checkout_queue.remove(kode)
        if kode in preorder_queue: preorder_queue.remove(kode)
        simpan_produk()
        print("✓ Produk dihapus!")

# ========== FITUR TAMBAHAN ==========
def generate_sku(kat):
    prefix = f"MKS-{kat[:3]}"
    if kat not in sku_stack: sku_stack[kat] = []
    stack = sku_stack[kat]
    nomor = 1 if not stack else int(stack[-1].split('-')[-1]) + 1
    sku = f"{prefix}-{nomor:03d}"
    stack.append(sku)
    return sku

def undo():
    print("\n=== UNDO AKSI ===")
    if not undo_stack:
        print("✗ Tidak ada aksi")
        return
    aksi = undo_stack.pop()
    if aksi['aksi'] == 'tambah':
        db.hapus(aksi['data']['kode_produk'])
        del hash_db[aksi['data']['kode_produk']]
        print(f"✓ Undo tambah {aksi['data']['nama_produk']}")
    elif aksi['aksi'] == 'hapus':
        db.tambah_depan(aksi['data'])
        hash_db[aksi['data']['kode_produk']] = aksi['data']
        print(f"✓ Undo hapus {aksi['data']['nama_produk']}")
    elif aksi['aksi'] == 'update':
        db.update(aksi['kode'], aksi['lama'])
        hash_db = aksi['lama']
        print(f"✓ Undo update {aksi['kode']}")
    simpan_produk()

def leaderboard():
    print("\n=== TOP 5 HARGA TERMAHAL ===")
    data = db.semua_data()
    data.sort(key=lambda x: x['harga_jual'], reverse=True) # Sorting
    if not data: print("Kosong")
    for i,p in enumerate(data[:5], 1):
        print(f"{i}. {p['nama_produk']} - Rp{p['harga_jual']:,}")

def restock():
    print("\n=== RESTOCK PREORDER ===")
    if not preorder_queue:
        print("Tidak ada preorder")
        return
    print(f"Antrian: {list(preorder_queue)}")
    kode = input("Kode yg direstock: ").upper()
    if kode in hash_db and hash_db['status'] == 'Preorder':
        tambah = int(input("Tambah stok: "))
        hash_db['stok'] += tambah
        hash_db['status'] = 'Tersedia'
        db.update(kode, hash_db)
        preorder_queue.remove(kode)
        checkout_queue.append(kode)
        simpan_produk()
        print(f"✓ {kode} berhasil direstock!")
    else:
        print("Kode salah/bukan preorder")

def tampil_semua():
    print("\n=== SEMUA PRODUK ===")
    data = db.semua_data()
    if not data: print("Kosong")
    for p in data:
        print(f"{p['kode_produk']} | {p['nama_produk'][:20]:20} | Stok:{p['stok']:3} | Rp{p['harga_jual']:,} | {p['status']}")

# ========== MENU ==========
def main():
    load_kategori()
    load_produk()

    while True:
        print("\n" + "="*45)
        print(" MARKETPLACE MAKEUP - FULL CRUD 2026")
        print("="*45)
        print("1. Tambah Produk [CREATE]")
        print("2. Cari Produk [READ/Hash]")
        print("3. Update Produk [UPDATE]")
        print("4. Hapus Produk [DELETE]")
        print("5. Lihat Semua [LinkedList]")
        print("6. Undo Aksi [Stack]")
        print("7. Top 5 Termahal [Sorting]")
        print("8. Restock Preorder [Queue]")
        print("9. Antrian Checkout [Queue]")
        print("0. Keluar")

        pilih = input("\nPilih: ").strip()

        if pilih == '1': create_produk()
        elif pilih == '2': read_produk()
        elif pilih == '3': update_produk()
        elif pilih == '4': delete_produk()
        elif pilih == '5': tampil_semua()
        elif pilih == '6': undo()
        elif pilih == '7': leaderboard()
        elif pilih == '8': restock()
        elif pilih == '9': print(f"Antrian: {list(checkout_queue)}")
        elif pilih == '0': break
        else: print("Pilihan salah!")

if __name__ == "__main__":
    main()