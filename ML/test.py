import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical

df = pd.read_csv('ML/data.csv')
df = df.fillna('')

LE = LabelEncoder()
df['category'] = LE.fit_transform(df['category'])

# Hedef değişkeni one-hot-encoding yap
y = to_categorical(df['category'])

# Ürün özelliklerini birleştir
df['features'] = df['category'].astype(str) + ' ' + df['product'] + ' ' + df['feature_0'] + ' ' + df['feature_1'] + ' ' + df['feature_2'] + ' ' + df['feature_3'] + ' ' + df['feature_4'] + ' ' + df['feature_5'] + ' ' + df['feature_6'] + ' ' + df['feature_7']

# TF-IDF vektörleme
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['features'])

# Özellikler matrisini oluştur
X = tfidf_matrix.toarray()  # TF-IDF vektörlerini yoğun bir matrise dönüştür

# Modeli oluştur
model = Sequential()
model.add(Dense(64, input_dim=X.shape[1], activation='relu'))
model.add(Dense(y.shape[1], activation='softmax'))

# Modeli derle
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Modeli eğit
model.fit(X, y, epochs=64, batch_size=32)

# Modeli kaydet
model.save('ML/recommendation_system.h5')

# Modeli yükle
from keras.models import load_model
model = load_model('ML/recommendation_system.h5')

# Cosine Similarity ile benzerlik matrisini hesapla
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Kullanıcının seçtiği ürünleri al
chosen_products = [
    'Philips 242e1gsj/27 23.8" 144hz 1ms Hdmı+dp Freesync Fullhd Va Oyuncu Monitörü T15498',
]
# Seçilen ürünlere benzer ürünlerin indexlerini ve benzerlik skorlarını al
similar_products = []
for product in chosen_products:
    product_index = df[df['product'] == product.strip()].index[0]
    similar_products += list(enumerate(cosine_sim[product_index]))

# Benzerlik skorlarına göre ürünleri sırala
sorted_similar_products = sorted(similar_products, key=lambda x:x[1], reverse=True)
# print(sorted_similar_products)
print("############### Ürün Önerileri ###############")
count = 0
for i in range(len(sorted_similar_products)):
    if df['product'][sorted_similar_products[i][0]] not in chosen_products:
        print(f"Score : {sorted_similar_products[i][1]} --- {df['product'][sorted_similar_products[i][0]]}")
        
        count += 1
        if count == 15:
            break
