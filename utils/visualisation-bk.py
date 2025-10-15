"""Plotting helpers.

* Aitoff sky map (Matplotlib)
* Wrapper for the pre‑existing `explain_local` function
"""
import matplotlib.pyplot as plt
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
import pandas as pd
import matplotlib.patches as patches
import seaborn as sns



# ----------------------------------------------------------------------
# Aitoff projection
# ----------------------------------------------------------------------
def plot_aitoff(df: pd.DataFrame):
    """Plot RA/Dec of the given sources on an Aitoff projection."""
    ra_rad = np.remainder(df["ra"] + 360, 360)  # shift RA values
    ra_rad = ra_rad * np.pi / 180.0
    ra_rad = -(ra_rad - np.pi)  # reverse direction for typical sky view
    dec_rad = df["dec"] * np.pi / 180.0

    fig = plt.figure(figsize=(8, 4.5))
    ax = fig.add_subplot(111, projection="aitoff")
    ax.scatter(ra_rad, dec_rad, s=20, c="tab:orange", alpha=0.7)
    ax.grid(True)
    ax.set_title("Selected sources (Aitoff projection)")
    return fig


# ----------------------------------------------------------------------
# Local explanation (placeholder – uses a mock implementation)
# ----------------------------------------------------------------------
# def explain_local(source_name: str, feature_df: pd.DataFrame):
#     """Generate a bar plot of feature contributions for a source.

#     In a real deployment this would call the user‑provided
#     `explain_local` function; here we simulate it.
#     """
#     contributions = feature_df.loc[source_name]
#     fig, ax = plt.subplots(figsize=(6, 3))
#     contributions.plot.bar(ax=ax, color="steelblue")
#     ax.set_ylabel("Contribution")
#     ax.set_title(f"Local explanation for {source_name}")
#     plt.tight_layout()
#     return fig


def get_local_shap(srcname: str, shap_df: pd.DataFrame):
    try:
        exsrc = shap_df.loc[srcname].to_frame(name='SHAP value') #example source
    except:
        return pd.DataFrame({"features" : [] , "importance" : [], 'contrib':[]})
    exsrc = exsrc.sort_values(by = 'SHAP value', ascending=False)
    exsrc.index.name = 'Feature'
    exsrc.index = [exi[:-5] for exi in exsrc.index.to_list()]
    exsrc['abs_value'] = exsrc.apply(lambda x: np.abs(x['SHAP value']), axis=1)
    exsrc = exsrc.sort_values(by = 'abs_value', ascending=False)
    exsrc.index.name = 'Feature'
    exsrc = exsrc.reset_index()
    features = exsrc.iloc[:10]['Feature'].to_list()
    features.append('ARF')
    features =  features[::-1]
    importance = exsrc.iloc[:10]['SHAP value'].to_list()
    importance.append(exsrc.iloc[10:]['SHAP value'].sum())
    importance = np.asarray(importance[::-1])
    fdf = pd.DataFrame({"features" : features , "importance" : importance , "contrib" : ["+ve" if i > 0 else "-ve" for i in importance]})
    fdf = fdf.set_index('features').sort_values('importance', ascending=False)
    f_indx = fdf.index.to_numpy()
    f_indx = f_indx[fdf.index.to_numpy()!='ARF']
    f_indx = list(f_indx)+list(['ARF'])
    fdf = fdf.loc[f_indx]
    # fdf.loc['ARF', 'contrib'] = 0
    return fdf.reset_index()



def explain_local(srcname: str, shap_df: pd.DataFrame):

    fdf = get_local_sap(srcname , shap_df)
    features = fdf['features'].to_numpy()
    importance = fdf['importance'].to_numpy()
    plt.rcParams.update({'font.size':10})
    fig = plt.figure(figsize=(12,6))

    ax = plt.subplot(111)
    clr = '#d10042'
    clr = 'teal'
    # ax = sns.barplot(exsrc.iloc[:10] , x = 'SHAP value', y='Feature', color='salmon',)
    bars = ax.barh(features, importance, color=clr, )
    ax.set_ylabel('')
    clr_list = [clr]*(len(importance)-1) +['gray']
    clr_list = clr_list[::-1]
    # Add value labels inside the bars
    for bar , f , imp ,c in zip(bars,features, importance, clr_list):
        if(imp>1): 
            txtloc = imp-0.25
            txtclr = 'white' 
            weig = 'bold'
        elif(imp<0): 
            txtloc = 0
            txtclr = 'k' 
            weig = None
            # c = 
        else:
            txtloc = imp + 0.1
            txtclr = 'black' 
            weig = None

        ax.text(txtloc, bar.get_y() + bar.get_height()/2,
                f'{imp:.2f}', ha='left', va='center', color=txtclr, fontsize=12, fontweight=weig)
        h = bar.get_height()
        # print(h)
        y = bar.get_y()
        x = 0
        height = 1
        width = 0.8
    # kum
        arrow_points = [ (imp-0.,y+0.8) , (imp,y) , (imp+0.03, y+0.4) ]
        arrow = patches.Polygon(arrow_points, facecolor=c, edgecolor=None)
        # print(c)
        ax.add_patch(arrow)
    # ax.yaxis_inverted()
    ax.axvline(x = 0, c = 'k')
    sns.despine()
    bars[0].set_color('gray')
    bars[0].set_height(0.8)
    sns.despine()
    ax.set_xlabel('SHAP Value (Contribution in model output)')
    # ax.patches[0].set
    ax.set_title(f'CSC-ID : {srcname}', fontsize = 12)
    return fig
    # plt.show()