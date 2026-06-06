import random
import time
import pandas as pd
import os
from dataProduk import getDataAsli, augmentData
from skorSAW import hitungSaw
from Greedy import algoritmaGreedy
from BranchnBound import algoritmaBranchAndBound
from HillClimbing import algoritmaHillClimbing

# KONFIGURASI GLOBAL
RANDOM_SEED = 42
JUMLAH_DATA_TARGET = 1000
JUMLAH_PENGUJIAN = 30
MAX_RESTART_HC = 10

def ukurPerformaAlgoritma(namaAlgoritma, fungsiAlgoritma, df, skorOptimal):
    daftarWaktu = []
    tokoTerbaik = None
    skorTerbaik = -1
    
    for _ in range(JUMLAH_PENGUJIAN):
        waktuMulai = time.perf_counter()
        hasil = fungsiAlgoritma(df)
        waktuSelesai = time.perf_counter()
        
        waktuMs = (waktuSelesai - waktuMulai) * 1000
        daftarWaktu.append(waktuMs)
        if isinstance(hasil, pd.Series):
            skorHasil = hasil["skorSAW"]
            namaToko = hasil["Toko"]
        else: 
            continue
            
        if skorHasil > skorTerbaik:
            skorTerbaik = skorHasil
            tokoTerbaik = namaToko

    rataRataWaktu = sum(daftarWaktu) / len(daftarWaktu)
    
    # Perhitungan Akurasi
    if skorOptimal > 0:
        akurasi = (skorTerbaik / skorOptimal) * 100
    else:
        akurasi = 0

    return {
        "Algoritma": namaAlgoritma,
        "Daftar Waktu": daftarWaktu,
        "Waktu Rata-rata (ms)": rataRataWaktu,
        "Toko Terpilih": tokoTerbaik,
        "Akurasi (%)": akurasi
    }

def simpanExcelLengkap(dfAugmented, dfFinal, hasilRekap, namaFile="Dataset_Lengkap_Proyek_ASA.xlsx"):
    if os.path.exists(namaFile):
        try:
            os.remove(namaFile)
        except PermissionError:
            print(f"[WARNING] Tutup file '{namaFile}' di Excel sebelum menjalankan script!")
            return

    try:
        with pd.ExcelWriter(namaFile, engine='openpyxl') as writer:
            # Sheet 1 - Data Hasil Augmentasi
            dfMentah = dfAugmented[['Kode', 'Toko', 'Harga', 'Rating']]
            dfMentah.to_excel(writer, sheet_name='Data_Hasil_Augmentasi', index=False)
            
            # Sheet 2 - Skor SAW
            dfSaw = dfFinal[['Kode', 'Toko', 'Harga', 'Rating', 'normHarga', 'normRating', 'skorSAW']]
            dfSaw = dfSaw.sort_values(by='skorSAW', ascending=False)
            dfSaw.to_excel(writer, sheet_name='Skor_SAW', index=False)
            
            # Sheet 3 - Data 30 Iterasi Performa
            dfIterasi = pd.DataFrame({
                "Iterasi_Ke": range(1, JUMLAH_PENGUJIAN + 1),
                "Waktu_Greedy_ms": hasilRekap[0]["Daftar Waktu"],
                "Waktu_BnB_ms": hasilRekap[1]["Daftar Waktu"],
                "Waktu_HC_ms": hasilRekap[2]["Daftar Waktu"]
            })
            dfIterasi.to_excel(writer, sheet_name='Data_30_Iterasi', index=False)
                    
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan Excel: {e}")

def main():
    random.seed(RANDOM_SEED)
    
    print("\n" + "="*60)
    print("PROYEK MAKALAH ANALISIS STRATEGI ALGORITMA")
    print("="*60)
    
    # Persiapan Data
    dfAsli = getDataAsli()
    dfAugmented = augmentData(dfAsli, JUMLAH_DATA_TARGET)
    print(f"      Data asli: {len(dfAsli)} toko.")
    print(f"      Data augmentasi: {len(dfAugmented)} toko.")
    
    # Hitung SAW
    dfFinal = hitungSaw(dfAugmented)
    
    # Top 5
    top5 = dfFinal.sort_values(by="skorSAW", ascending=False).head(5)
    print("      Top 5 Toko Terbaik:")
    for i, (_, row) in enumerate(top5.iterrows(), start=1):
        print(f"      {i}. {row['Toko']} (Skor: {row['skorSAW']:.4f})")
        
    refResult = algoritmaBranchAndBound(dfFinal)
    skorOptimal = refResult["skorSAW"]
    tokoOptimal = refResult["Toko"]
    print(f"      Solusi Optimal: {tokoOptimal}")
    print(f"      Skor Optimal: {skorOptimal:.6f}")
    
    print(f"      Jumlah pengujian: {JUMLAH_PENGUJIAN} kali per algoritma")    
    daftarAlgoritma = [
        ("Greedy", algoritmaGreedy),
        ("Branch and Bound", algoritmaBranchAndBound),
        ("Hill Climbing", lambda df: algoritmaHillClimbing(df, MAX_RESTART_HC))
    ]
    
    hasilRekap = []
    for nama, fungsi in daftarAlgoritma:
        print(f"      Sedang menguji {nama} ...")
        hasil = ukurPerformaAlgoritma(nama, fungsi, dfFinal, skorOptimal)
        hasilRekap.append(hasil)

    print("\n" + "="*60)
    print("HASIL AKHIR")
    print("="*60)
    header = f"{'Algoritma':<20} {'Toko Terpilih':<25} {'Rata-rata (ms)':>15} {'Akurasi':>10}"
    print(header)
    print("-" * len(header))
    for h in hasilRekap:
        print(
            f"{h['Algoritma']:<20} "
            f"{h['Toko Terpilih']:<25} "
            f"{h['Waktu Rata-rata (ms)']:>15.4f} "
            f"{h['Akurasi (%)']:>9.2f}%"
        )
        
    print("="*60)
    simpanExcelLengkap(dfAugmented, dfFinal, hasilRekap)

if __name__ == "__main__":
    main()