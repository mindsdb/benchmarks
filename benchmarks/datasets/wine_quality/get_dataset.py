import numpy as np
import pandas as pd

if __name__ == '__main__':
    red = pd.read_csv("red.csv", sep=";")
    white = pd.read_csv("white.csv", sep=";")

    df = pd.concat([white, red], ignore_index=True)

    df.columns = ['fixed_acidity',
                  'volatile_acidity',
                  'citric_acid',
                  'residual_sugar',
                  'chlorides',
                  'free_sulfur_dioxide',
                  'total_sulfur_dioxide',
                  'density',
                  'pH',
                  'sulphates',
                  'alcohol',
                  'quality']

    df.to_csv("data.csv", sep=",", index_label='id')
