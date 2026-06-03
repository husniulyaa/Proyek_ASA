import pandas as pd


data_shopee = {
    "Kode": [
        "T1", "T2", "T3", "T4", "T5",
        "T6", "T7", "T8", "T9", "T10",
        "T11", "T12", "T13", "T14", "T15",
        "T16", "T17", "T18", "T19", "T20",
        "T21", "T22", "T23", "T24", "T25"
    ],
    "Toko": [
        "Sea Makeup",
        "Guardian Beauty",
        "Beautyhaul",
        "Serene Kosmetik",
        "hellonoonaa.co",
        "Jeolla_Shop",
        "Guzel Beaute",
        "GlowUp.id",
        "BeautyVault",
        "Kosmetik Smg",
        "Cantiqa Beauty",
        "Sociolla Beauty",
        "Lippieland",
        "Makeup JKT",
        "BeautyCorner",
        "ChicGlow",
        "Rumah Cantik",
        "SkincareMakeup",
        "Velvet Beauty",
        "Nona Kosmetik",
        "Dewi Beauty",
        "PrettyMe",
        "Aurora Beauty",
        "Laras Kosmetik",
        "Belleza Makeup"
    ],
    "Harga": [
        56350, 59000, 51100, 53000, 51186,
        49999, 54999, 48500, 52999, 51200,
        57500, 61500, 46850, 55250, 49900,
        58999, 47600, 53500, 60250, 51550,
        49250, 54800, 46750, 58200, 50500
    ],
    "Rating": [
        4.9, 4.8, 4.9, 4.9, 4.9,
        4.8, 4.8, 4.8, 4.9, 4.7,
        4.8, 5.0, 4.6, 4.9, 4.8,
        4.7, 4.9, 4.8, 4.9, 4.7,
        4.8, 4.9, 4.6, 5.0, 4.8
    ]
}

df = pd.DataFrame(data_shopee)
