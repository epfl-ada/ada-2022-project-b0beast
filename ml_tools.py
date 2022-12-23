import pandas as pd
import numpy as np
import ast
import datetime
import pickle

from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

def standardize_column(dataset, column, mean, std):
    df = dataset.copy()
    df[column] = (df[column] - mean) / std
    return df

def destandardize_column(dataset, column, mean, std):
    df = dataset.copy()
    df[column] = df[column] * std + mean
    return df

def normalize_column(dataset, column, min, max):
    df = dataset.copy()
    df[column] = (df[column] - min) / (max - min)
    return df

def denormalize_column(dataset, column, min, max):
    df = dataset.copy()
    df[column] = df[column] * (max - min) + min
    return df

def standardize(dataset, columns, means, stds):
    df = dataset.copy()
    for column in columns:
        df = standardize_column(df, column, means[column], stds[column])
    return df

def destandardize(dataset, columns, means, stds):
    df = dataset.copy()
    for column in columns:
        df = destandardize_column(df, column, means[column], stds[column])
    return df

def normalize(dataset, columns, mins, maxs):
    df = dataset.copy()
    for column in columns:
        df = normalize_column(df, column, mins[column], maxs[column])
    return df

def denormalize(dataset, columns, mins, maxs):
    df = dataset.copy()
    for column in columns:
        df = denormalize_column(df, column, mins[column], maxs[column])
    return df