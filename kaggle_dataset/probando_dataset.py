import kaggle

# Nombre del dataset (búscalo en Kaggle)
dataset_name = "airbnb/seattle"

# Descargar el dataset en la carpeta actual
kaggle.api.dataset_download_files(dataset_name, path="./", unzip=True)

print(f"✅ Dataset '{dataset_name}' descargado correctamente.")