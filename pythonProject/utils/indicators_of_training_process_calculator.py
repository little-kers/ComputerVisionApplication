import numpy as np
from sklearn.metrics import recall_score, roc_curve, auc
import matplotlib.pyplot as plt


def precision(prediction, pre_labels):
    prediction_integers = (prediction > 0.5).astype(int)  # 将概率值转换为二分类标签
    tp = ((prediction_integers == 1) & (pre_labels == 1)).sum()  # 统计真正为正例的样本数
    fp = ((prediction_integers == 1) & (pre_labels == 0)).sum()  # 统计被错误预测为正例的样本数
    positive = tp + fp
    pre = np.sum(prediction_integers) / positive
    return pre


def recall_calc(target, predict):
    r = recall_score(y_true=target, y_pred=np.argmax(predict, axis=1))
    return r


def auc_calc(data_labels, predictions):
    fpr, tpr, thresholds = roc_curve(data_labels, predictions)
    roc_auc = auc(fpr, tpr)
    print('AUC:', roc_auc)
    return roc_auc, fpr, tpr


def show_roc(roc_auc, fpr, tpr, save_path=None):
    plt.figure(figsize=(10, 6))
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.savefig(f"{save_path}/Receiver operating characteristic example.png")
    plt.show()
