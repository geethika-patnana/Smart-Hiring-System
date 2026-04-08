"""
Metrics Utilities
Custom metrics and evaluation functions
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score, matthews_corrcoef
)

def calculate_all_metrics(y_true, y_pred, y_pred_proba=None):
    """
    Calculate comprehensive set of metrics
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        y_pred_proba: Predicted probabilities (optional)
    
    Returns:
        Dictionary of metrics
    """
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
        'recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
        'f1_score': f1_score(y_true, y_pred, average='weighted', zero_division=0),
        'mcc': matthews_corrcoef(y_true, y_pred)
    }
    
    if y_pred_proba is not None and len(np.unique(y_true)) == 2:
        metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba[:, 1])
    
    return metrics

def calculate_sensitivity_specificity(y_true, y_pred):
    """
    Calculate sensitivity and specificity (for binary classification)
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
    
    Returns:
        Tuple of (sensitivity, specificity)
    """
    cm = confusion_matrix(y_true, y_pred)
    
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        return sensitivity, specificity
    else:
        return None, None

def print_metrics_summary(metrics):
    """
    Print formatted metrics summary
    
    Args:
        metrics: Dictionary of metrics
    """
    print("\n" + "="*50)
    print("METRICS SUMMARY")
    print("="*50)
    
    for metric_name, value in metrics.items():
        print(f"{metric_name.replace('_', ' ').title():.<30} {value:.4f}")
    
    print("="*50)
