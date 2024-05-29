# Yiğit Leblebicier 2012721035
# Fatma Yılmaz 2012721037
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error
from pandas import read_csv, get_dummies, DataFrame
from joblib import dump, load
import json
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
import numpy as np
import pandas as pd

def calculate_vif(data):
    """
    Verilen veri setindeki her bir bağımsız değişken için VIF hesaplar.

    Parametreler:
    - data (DataFrame): Bağımsız değişkenleri içeren veri seti.

    Döndürülenler:
    - vif_data (DataFrame): Bağımsız değişkenler ve ilgili VIF değerlerini içeren DataFrame.
    """
    # NaN ve sonsuz değerleri kontrol et ve kaldır
    data = data.replace([np.inf, -np.inf], np.nan).dropna()

    # Sadece sayısal sütunları seç
    data = data.select_dtypes(include=[np.number])

    # Sabit terim ekle
    X = add_constant(data)
    vif_data = pd.DataFrame()
    vif_data["feature"] = X.columns
    vif_data["VIF"] = [
        variance_inflation_factor(X.values, i) for i in range(X.shape[1])
    ]
    return vif_data

def multiple_linear_regression(
    dataset_path: str,
    save_path: str,
    test_size: float = 0.2,
    random_state: int = 42,
):
    """
    Verilen veri seti üzerinde çoklu doğrusal regresyon uygular.

    Parametreler:
    - dataset_path (str): Veri setinin CSV dosya yolu.
    - save_path (str): Eğitilen model ve metriklerin kaydedileceği yol.
    - test_size (float): Veri setinin test bölümü için ayrılacak oranı.
    - random_state (int): Rastgele sayı üreteci için kullanılan tohum.

    Döndürülenler:
    - mse (float): Modelin Ortalama Kare Hatası.
    - r2 (float): Modelin R-kare değeri.
    - mape (float): Modelin Ortalama Mutlak Yüzde Hatası.
    - vif (str): Modelin kararlılığı ('Stable' veya 'Unstable').
    """
    try:
        # Veri setini yükle
        dataset = read_csv(dataset_path)

        # Özellikler ve hedef değişkeni hazırla
        X = dataset.iloc[:, :-1]
        y = dataset.iloc[:, -1]

        # Hedef değişkende NaN olan satırları çıkar
        valid_indices = y.notna()
        X = X[valid_indices]
        y = y[valid_indices]

        # Kategorik değişkenleri one-hot encode et
        X = get_dummies(X, drop_first=True)

        # VIF hesapla
        vif = calculate_vif(X)

        # VIF değerleri yüksek olan değişkenleri kontrol et
        high_vif_features = vif[vif["VIF"] > 10]["feature"]
        # Sabit terimi hariç tutarak kararlılık kontrolü
        high_vif_features = high_vif_features[high_vif_features != "const"]
        if not high_vif_features.empty:
            vif_status = "Unstable"
        else:
            vif_status = "Stable"

        # Veri setini eğitim ve test setlerine ayır
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        # Modeli başlat ve eğit
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Test setinde tahminler yap
        y_pred = model.predict(X_test)

        # Modeli değerlendir
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        mape = mean_absolute_percentage_error(y_test, y_pred) * 100

        # Modeli ve eğitim sırasında kullanılan sütunları kaydet
        dump((model, X.columns.tolist()), save_path)

        # Değerlendirme metriklerini JSON dosyasına kaydet
        metrics_path = save_path.replace(".pkl", "_metrics.json")
        with open(metrics_path, "w") as f:
            json.dump(
                {"mse": mse, "r2": r2, "mape": mape, "vif": vif_status}, f
            )

        return mse, r2, mape, vif_status, ", ".join(high_vif_features.tolist())
    except Exception as e:
        print(f"An error occurred during model training: {e}")
        return None, None, None, None

def predict_with_model(model_path: str, input: DataFrame):
    """
    Eğitilen bir model kullanarak hedef değerleri tahmin eder.

    Parametreler:
    - model_path (str): Kaydedilen model dosyasının yolu.
    - input (DataFrame): Tahmin için giriş verisi.

    Döndürülenler:
    - predictions (list): Tahmin edilen değerlerin listesi.
    """
    try:
        # Modeli ve sütun adlarını yükle
        model, model_columns = load(model_path)

        # Giriş verisini one-hot encode et
        new_data_processed = get_dummies(input, drop_first=True)

        # Eksik sütunları varsayılan değer olarak 0 ile ekle
        for column in model_columns:
            if column not in new_data_processed.columns:
                new_data_processed[column] = 0

        # Sütunları eğitim verisine uygun şekilde sırala
        new_data_processed = new_data_processed[model_columns]

        # Yüklenen modeli kullanarak tahmin yap
        predictions = model.predict(new_data_processed).tolist()

        return predictions
    except Exception as e:
        print(f"An error occurred during prediction: {e}")
        return None

def load_model_metrics(model_path: str):
    """
    Eğitilen bir modelin değerlendirme metriklerini yükler.

    Parametreler:
    - model_path (str): Kaydedilen model dosyasının yolu.

    Döndürülenler:
    - metrics (dict): Değerlendirme metriklerini içeren sözlük.
    """
    try:
        # Değerlendirme metriklerini JSON dosyasından yükle
        metrics_path = model_path.replace(".pkl", "_metrics.json")
        with open(metrics_path, "r") as f:
            metrics = json.load(f)
        return metrics
    except Exception as e:
        print(f"An error occurred while loading metrics: {e}")
        return None
