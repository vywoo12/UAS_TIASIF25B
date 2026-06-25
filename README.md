# MARKETPLACE MAKEUP - SISTEM CRUD PYTHON
### UAS Struktur Data 2026

Sistem manajemen produk marketplace makeup berbasis CLI dengan implementasi 4 struktur data: Linked List, Hash Map, Stack, Queue + Sorting.

---
### Flowchart
![alt text](https://github.com/vywoo12/UAS_TIASIF25B/blob/main/TIAS%20FLOWCHART%20UAS.jpeg?raw=true)

### **1. DESKRIPSI SINGKAT**
Program ini digunakan untuk mengelola data produk makeup dengan fitur CRUD lengkap. Data disimpan di file CSV dan dimuat ke memory menggunakan struktur data agar operasi cepat dan efisien.

**Struktur Data yg Diimplementasikan:**
1. **Linked List** → Menyimpan semua data produk secara berurutan. Dipakai buat traversal "Lihat Semua Produk"
2. **Hash Map / Dictionary** → Key = `kode_produk`, Value = data produk. Dipakai buat "Cari Produk" O(1)
3. **Stack LIFO** → Dipakai buat 2 hal: 
   - Generate SKU otomatis per kategori
   - Fitur Undo aksi terakhir: tambah/hapus/update
4. **Queue FIFO** → Dipakai buat antrian:
   - `checkout_queue` : Produk yg stok > 0, siap dijual
   - `preorder_queue` : Produk yg stok = 0, nunggu restock
5. **Sorting** → Menu Leaderboard Top 5 produk termahal

---

### **2. FITUR PROGRAM**
| Menu | Nama Fitur | Struktur Data | Keterangan |
| --- | --- | --- | --- |
| 1 | Tambah Produk [CREATE] | LinkedList + Hash + Stack + Queue | Input produk baru, auto generate SKU & status |
| 2 | Cari Produk [READ] | Hash Map | Cari by kode produk, output O(1) |
| 3 | Update Produk [UPDATE] | LinkedList + Hash + Stack | Edit nama/stok/harga, auto backup ke undo |
| 4 | Hapus Produk [DELETE] | LinkedList + Hash + Stack + Queue | Hapus + konfirmasi + backup undo |
| 5 | Lihat Semua [VIEW] | LinkedList | Traverse dari head ke tail |
| 6 | Undo Aksi [STACK] | Stack LIFO | Batalkan aksi tambah/hapus/update terakhir |
| 7 | Top 5 Termahal [SORT] | LinkedList + Sorting | Sorting descending by harga_jual |
| 8 | Restock Preorder [QUEUE] | Queue FIFO | Pindahkan dari preorder ke checkout |
| 9 | Lihat Antrian Checkout | Queue FIFO | Tampilkan antrian produk siap jual |
| 0 | Keluar | - | Simpan semua data ke CSV |

---

### **3. CARA INSTALASI & MENJALANKAN**
1. **Syarat**: Python 3.8+ terinstall
2. **File yg dibutuhkan**: Taruh 3 file ini di 1 folder
