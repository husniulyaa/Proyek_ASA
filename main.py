import random
import time
import pandas as pd

from BranchnBound import BranchandBound
from Greedy import Greedy
from HillClimbing import HillClimbing
from dataProduk import df as dataShopee
from skorSAW import hitung_saw

jumlahPengujian = 10
def ambilNamaToko(hasil):
    if isinstance(hasil, pd.Series):
        return hasil["Toko"]
    return hasil

def ambilSkorToko(df, namaToko):
    barisToko = df[df["Toko"] == namaToko]
    if barisToko.empty:
        return 0
    return barisToko.iloc[0]["skorSAW"]

def ukurAlgoritma(namaAlgoritma, fungsiAlgoritma, df, skorOptimal):
    totalWaktu = 0
    tokoTerbaik = None
    skorTerbaik = -1
    for i in range(jumlahPengujian):
        startTime = time.perf_counter()
        hasil = fungsiAlgoritma(df)
        endTime = time.perf_counter()

        waktuMs = (endTime - startTime) * 1000
        tokoTerpilih = ambilNamaToko(hasil)
        skorTerpilih = ambilSkorToko(df, tokoTerpilih)
        totalWaktu += waktuMs

        if skorTerpilih > skorTerbaik:
            skorTerbaik = skorTerpilih
            tokoTerbaik = tokoTerpilih
    akurasi = (skorTerbaik/skorOptimal) * 100 if skorOptimal > 0 else 0
    return {
        "Nama Algoritma": namaAlgoritma,
        "Rata-rata Waktu Eksekusi (ms)": totalWaktu/jumlahPengujian,
        "Toko yang Dipilih": tokoTerbaik,
        "Akurasi (%)": akurasi
    }

def cetakTabelRekapitulasi(hasilRekap):
    header = (
        f"{'Nama Algoritma':<20}"
        f"{'Rata-rata Waktu Eksekusi (ms)':>34}  "
        f"{'Toko yang Dipilih':<30}"
        f"{'Akurasi (%)':>14}"
    )
    garis = "-" * len(header)
    print("TABEL HASIL PENGUJIAN")
    print(garis)
    print(header)
    print(garis)
    for hasil in hasilRekap:
        print(
            f"{hasil['Nama Algoritma']:<20}"
            f"{hasil['Rata-rata Waktu Eksekusi (ms)']:>34.6f}  "
            f"{hasil['Toko yang Dipilih']:<30}"
            f"{hasil['Akurasi (%)']:>14.2f}"
        )
    print(garis)

def main():
    random.seed(42)
    df = hitung_saw(dataShopee.copy())
    tokoOptimal = BranchandBound(df)
    skorOptimal = ambilSkorToko(df, tokoOptimal)
    algoritma = [
        ("Greedy", Greedy),
        ("Branch and Bound", BranchandBound),
        ("Hill Climbing", HillClimbing)
    ]

    hasilRekap = []
    for namaAlgoritma, fungsiAlgoritma in algoritma:
        hasilRekap.append(
            ukurAlgoritma(namaAlgoritma, fungsiAlgoritma, df, skorOptimal)
        )

    print(f"Jumlah data yang diuji: {len(df)} toko")
    print(f"Solusi optimal pembanding: {tokoOptimal}")
    print(f"Skor SAW optimal: {skorOptimal:.6f}\n")
    cetakTabelRekapitulasi(hasilRekap)

if __name__ == "__main__":
    main()
