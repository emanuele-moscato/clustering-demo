import numpy as np
import pandas as pd
import requests
from configparser import ConfigParser
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def get_data():
    confpars = ConfigParser()
    confpars.read('../.credentials/credentials.ini')
    endpoint = '/get_data'
    headers = {
            confpars['data_api']['header_key']: confpars['data_api']['api_key']
        }
    response = requests.get(
        url = confpars['data_api']['url']+endpoint,
        headers = headers
    )
    data_df = pd.DataFrame(response.json())
    data_df = data_df.reset_index()
    data_df = data_df.drop('index', axis=1)
    
    return data_df
    
def dim_reduce(data_df):
    X = np.array(data_df)
    pca_dimred = PCA(n_components=2)
    X_red = pca_dimred.fit_transform(X)
    scaler = StandardScaler()
    X_red = scaler.fit_transform(X_red)
    
    return X_red

def clusterize(X_red, n_clusters):
    kmeans_clustering = KMeans(n_clusters=n_clusters, random_state=42)
    clusters_pred = kmeans_clustering.fit_predict(X_red)
    clusters_df = pd.DataFrame({
        'x_red': X_red[:,0],
        'y_red': X_red[:,1],
        'cluster': clusters_pred
    })
    
    return clusters_df