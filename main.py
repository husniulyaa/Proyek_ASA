import random
import time
import pandas as pd
from dataProduk import getDataAsli, augmentData
from skorSAW import hitungSaw
from Greedy import algoritmaGreedy
from BranchnBound import algoritmaBranchAndBound
from HillClimbing import algoritmaHillClimbing

#konfigurasi global
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

    rataRataWaktu = sum(daftarWaktu)/len(daftarWaktu)
    akurasi = (skorTerbaik/skorOptimal) * 100
    if skorOptimal > 0:
        akurasi = (skorTerbaik/skorOptimal) * 100
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
    with pd.ExcelWriter(namaFile, engine="openpyxl") as writer:
        dfMentah = dfAugmented[["Kode Toko", "Toko", "Harga", "Rating"]]
        dfMentah.to_excel(writer, sheet_name="Data Hasil Augmentasi", index=False)
        
        dfSaw = dfFinal[["Kode Toko", "Toko", "Harga", "Rating", "normHarga", "normRating", "skorSAW"]]
        dfSaw = dfSaw.sort_values(by="skorSAW", ascending=False)
        dfSaw.to_excel(writer, sheet_name="Skor SAW", index=False)
        
        dfIterasi = pd.DataFrame({
            "Iterasi ke-": range(1, JUMLAH_PENGUJIAN + 1),
            "Waktu Greedy (ms)": hasilRekap[0]["Daftar Waktu"],
            "Waktu Branch and Bound (ms)": hasilRekap[1]["Daftar Waktu"],
            "Waktu Hill Climbing (ms)": hasilRekap[2]["Daftar Waktu"]
        })
        dfIterasi.to_excel(writer, sheet_name="Data 30 Iterasi", index=False)

    print("File tersimpan.")

def main():
    random.seed(RANDOM_SEED)
    print("\n" + "="*50)
    print("Analisis Algoritma")
    print("="*50)
    
    dfAsli = getDataAsli()
    dfAugmented = augmentData(dfAsli, JUMLAH_DATA_TARGET)
    print(f"Original: {len(dfAsli)} | Augmented: {len(dfAugmented)}")

    dfFinal = hitungSaw(dfAugmented)    
    top5Toko = dfFinal.sort_values(by="skorSAW", ascending=False).head(5)
    print("Top 5:")
    for urutan, (_, toko) in enumerate(top5Toko.iterrows(), start=1):
        print(f"      {urutan}. {toko['Toko']}: {toko['skorSAW']:.4f}")
        
    hasilReferensi = algoritmaBranchAndBound(dfFinal)
    skorOptimal = hasilReferensi["skorSAW"]
    tokoOptimal = hasilReferensi["Toko"]
    print(f"    Best: {tokoOptimal} ({skorOptimal:.4f})")
    
    daftarAlgoritma = [
        ("Greedy", algoritmaGreedy),
        ("Branch and Bound", algoritmaBranchAndBound),
        ("Hill Climbing", lambda df: algoritmaHillClimbing(df, MAX_RESTART_HC))
    ]
    
    hasilRekap = []
    for nama, fungsi in daftarAlgoritma:
        hasil = ukurPerformaAlgoritma(nama, fungsi, dfFinal, skorOptimal)
        hasilRekap.append(hasil)
        
    print("\n" + "="*50)
    print("Results")
    print("="*50)
    
    header = f"{'Algorithm':<20} {'Best Shop':<25} {'Avg (ms)':>12} {'Accuracy':>10}"
    print(header)
    print("-" * len(header))
    
    for hasil in hasilRekap:
        print(
            f"{hasil['Algoritma']:<20} "
            f"{hasil['Toko Terpilih']:<25} "
            f"{hasil['Waktu Rata-rata (ms)']:>12.2f} "
            f"{hasil['Akurasi (%)']:>10.1f}%"
        )
        
    print("="*50)
    try:
        simpanExcelLengkap(dfAugmented, dfFinal, hasilRekap)
    except Exception as error:
        print(f"Gagal menyimpan file: {error}")

# Main Program
main()

