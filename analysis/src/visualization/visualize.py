import matplotlib.pyplot as plt
import numpy as np

def pdf_cdf(ax, x, bins, normed=False, stats=True):
    
    v = plt.get_cmap('viridis')
    pdf_c = v.colors[0]
    cdf_c = v.colors[90]
    mean_c = v.colors[180]
    med_c = v.colors[230]
    
    xmax = np.max(x)
    xmin = np.min(x)

    pdf, bin_edges = np.histogram(x, bins)
    cdf = np.cumsum(pdf / np.sum(pdf))
    if normed:
        ax.set_ylabel('Probability')
        ax.bar(bin_edges[:-1], pdf / np.sum(pdf), np.diff(bin_edges), color=pdf_c)
    else:
        ax.set_ylabel('Frequency')
        ax.bar(bin_edges[:-1], pdf, np.diff(bin_edges), color=pdf_c)
    if stats:
        mean = np.mean(x)
        median = np.median(x)
        ax.axvline(mean, color=mean_c, linestyle='--', linewidth=3, label='Mean: {:.2f}'.format(mean), alpha=0.7)
        ax.axvline(median, color=med_c, linestyle='--', linewidth=3, label='Median: {:.2f}'.format(median), alpha=0.7)
        ax.legend()
    ax.set_xlim((np.min(bin_edges), np.max(bin_edges)))
    ax_cdf = ax.twinx()
    ax_cdf.plot(bin_edges[:-1], cdf, color=cdf_c, linewidth=4, alpha=0.8)
    ax_cdf.set_ylabel('Cumulative')
    ax_cdf.set_ylim((0, 1))
    ax_cdf.tick_params('y')
    return ax, ax_cdf
    
def pdf_cdf_h(ax, y, bins, normed=False, stats=True):
    v = plt.get_cmap('viridis')
    pdf_c = v.colors[0]
    cdf_c = v.colors[90]
    mean_c = v.colors[180]
    med_c = v.colors[230]
    
    xmax = np.max(y)
    xmin = np.min(y)

    pdf, bin_edges = np.histogram(y, bins)
    cdf = np.cumsum(pdf / np.sum(pdf))
    if normed:
        ax.set_xlabel('Probability')
        ax.barh(bin_edges[:-1], pdf / np.sum(pdf), np.diff(bin_edges), color=pdf_c)
    else:
        ax.set_xlabel('Frequency')
        ax.barh(bin_edges[:-1], pdf, np.diff(bin_edges), color=pdf_c)
    if stats:
        mean = np.mean(y)
        median = np.median(y)
        ax.axhline(mean, color=mean_c, linestyle='--', linewidth=3, label='Mean: {:.2f}'.format(mean), alpha=0.7)
        ax.axhline(median, color=med_c, linestyle='--', linewidth=3, label='Median: {:.2f}'.format(median), alpha=0.7)
        ax.legend()
    ax.set_ylim((np.min(bin_edges), np.max(bin_edges)))
    ax_cdf = ax.twiny()
    ax_cdf.plot(cdf, bin_edges[:-1], color=cdf_c, linewidth=4, alpha=0.8)
    ax_cdf.set_xlabel('Cumulative')
    ax_cdf.set_xlim((0, 1))
    ax_cdf.tick_params('y')
    return ax, ax_cdf
