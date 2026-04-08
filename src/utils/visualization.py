"""
Visualization Utilities
Common plotting functions for ML projects
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

def plot_feature_importance(feature_names, importances, top_n=20):
    """
    Plot feature importance
    
    Args:
        feature_names: List of feature names
        importances: Feature importance values
        top_n: Number of top features to display
    """
    indices = np.argsort(importances)[::-1][:top_n]
    
    plt.figure(figsize=(12, 8))
    plt.barh(range(top_n), importances[indices], color='steelblue')
    plt.yticks(range(top_n), [feature_names[i] for i in indices])
    plt.xlabel('Importance', fontsize=12)
    plt.title(f'Top {top_n} Feature Importances', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    
    return plt.gcf()

def plot_training_history(history):
    """
    Plot training history for deep learning models
    
    Args:
        history: Training history object from model.fit()
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    axes[0].plot(history.history['accuracy'], label='Train Accuracy')
    axes[0].plot(history.history['val_accuracy'], label='Val Accuracy')
    axes[0].set_title('Model Accuracy', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Accuracy')
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    axes[1].plot(history.history['loss'], label='Train Loss')
    axes[1].plot(history.history['val_loss'], label='Val Loss')
    axes[1].set_title('Model Loss', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Loss')
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    return fig

def plot_class_distribution(y, class_names=None):
    """
    Plot class distribution
    
    Args:
        y: Target labels
        class_names: Names of classes (optional)
    """
    unique, counts = np.unique(y, return_counts=True)
    
    if class_names is None:
        class_names = [f'Class {i}' for i in unique]
    
    fig = go.Figure(data=[
        go.Bar(x=class_names, y=counts, marker_color='steelblue')
    ])
    
    fig.update_layout(
        title='Class Distribution',
        xaxis_title='Class',
        yaxis_title='Count',
        template='plotly_white'
    )
    
    return fig

def plot_correlation_matrix(df, figsize=(12, 10)):
    """
    Plot correlation matrix heatmap
    
    Args:
        df: DataFrame with numeric features
        figsize: Figure size
    """
    corr = df.corr()
    
    plt.figure(figsize=figsize)
    sns.heatmap(
        corr, annot=True, fmt='.2f', cmap='coolwarm',
        center=0, square=True, linewidths=1
    )
    plt.title('Feature Correlation Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return plt.gcf()

def plot_model_comparison(results_dict):
    """
    Plot comparison of multiple models
    
    Args:
        results_dict: Dictionary with model names as keys and metrics as values
    """
    df = pd.DataFrame(results_dict).T
    
    metrics = ['test_accuracy', 'precision', 'recall', 'f1_score']
    available_metrics = [m for m in metrics if m in df.columns]
    
    fig = go.Figure()
    
    for metric in available_metrics:
        fig.add_trace(go.Bar(
            name=metric.replace('_', ' ').title(),
            x=df.index,
            y=df[metric]
        ))
    
    fig.update_layout(
        title='Model Performance Comparison',
        xaxis_title='Model',
        yaxis_title='Score',
        barmode='group',
        template='plotly_white',
        height=500
    )
    
    return fig
