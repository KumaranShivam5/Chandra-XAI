# utils/visualisation.py
"""
Plotly based visualisation helpers for the Chandra‑XAI Streamlit app.

Functions
---------
* plot_aitoff(selected_df) → plotly.graph_objects.Figure
* explain_local(source_name, feature_df) → plotly.graph_objects.Figure
"""
from __future__ import annotations

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from astropy import units as u
from astropy.coordinates import SkyCoord

from matplotlib import pyplot as plt

def plot_aitoff_mpl(selected_df: pd.DataFrame):
    """Plot RA/Dec of the given sources on an Aitoff projection."""
    # ra_rad = np.remainder(selected_df["ra"] + 360, 360)  # shift RA values
    # ra_rad = ra_rad * np.pi / 180.0
    # ra_rad = -(ra_rad - np.pi)  # reverse direction for typical sky view
    # dec_rad = selected_df["dec"] * np.pi / 180.0

    fig = plt.figure(figsize=(8, 4.5))
    ax = fig.add_subplot(111, projection="aitoff")
    ra = selected_df["ra"]*u.deg
    dec = selected_df["dec"]*u.deg

    eq = SkyCoord(selected_df['ra'].to_list() , selected_df['dec'].to_list() , unit = u.deg).galactic 
    l  = eq.l.wrap_at('180d').radian
    b = eq.b.radian

    ax.scatter(l, b , s = 4)

    return fig


import matplotlib.pyplot as plt
import matplotlib as mpl
import astropy.units as u
from astropy.coordinates import SkyCoord
import pandas as pd

colors_dict = {
'AGN':"lightsalmon", 'STAR': "#6ac7ff", 'YSO': "yellow", 'HMXB': "fuchsia",
'LMXB': "cyan", 'CV' : "aquamarine", 'ULX': "white", 'PULSAR': "pink"
}
@st.cache_data
@st.cache_resource
def plot_aitoff_mpl_dark(selected_df: pd.DataFrame,
                         *,
                         figsize: tuple = (8, 4),
                         point_size: float = 24,
                         point_size_scale : 2,
                         point_color: str = "#ffcc00",   # bright amber that shows well on black
                         background_color: str = "#212121",  # very dark gray (almost pure black)
                         grid_color: str = "teal",    # subtle grey grid lines
                         label_color: str = "#ffffff") -> plt.Figure:
    """
    Plot RA/Dec of the given sources on an Aitoff projection **with a dark theme**.

    Parameters
    ----------
    selected_df : pd.DataFrame
        Must contain the columns ``ra`` and ``dec`` (in decimal degrees).  
        The index is **not** used – the function extracts the values directly.
    figsize : tuple, optional
        Width × height of the figure (default = (8, 4.5)).
    point_size : float, optional
        Marker size passed to ``ax.scatter`` (default = 4).
    point_color : str, optional
        Hex colour (or any Matplotlib colour spec) for the points.  
        Choose something bright that contrasts with a black background.
    background_color : str, optional
        Figure/axes background colour (default = very dark gray).
    grid_color : str, optional
        Colour of the longitude/latitude grid lines.
    label_color : str, optional
        Colour of axis labels, tick labels and the title.

    Returns
    -------
    matplotlib.figure.Figure
        A Matplotlib figure that you can display with ``st.pyplot(fig)`` in
        Streamlit or with ``fig.show()`` in a notebook.
    """
    # ----------------------------------------------------------------------
    # 0️⃣  Switch to a dark style **only for this figure**
    # ----------------------------------------------------------------------
    # We do the styling *inside* the function so that the rest of your
    # app (or any other Matplotlib plot) can stay in the default (light) style.
    # ----------------------------------------------------------------------
    # Store the current rcParams so we can restore them later – this prevents
    # the dark colours from leaking into other figures that you may create
    # elsewhere in the same Python process.
    old_rc = mpl.rcParams.copy()

    # ---- dark‑mode rcParams ------------------------------------------------
    dark_style = {
        # Figure & axes background
        "figure.facecolor": background_color,
        "axes.facecolor":   background_color,
        # Text / tick colours
        "text.color":       label_color,
        "axes.labelcolor":  label_color,
        "xtick.color":      label_color,
        "ytick.color":      label_color,
        # Grid line colour
        "grid.color":       grid_color,
        # Spines (the outer frame) – we hide them because the Aitoff projection
        # already draws a circular border.
        "axes.edgecolor":   'teal',
        # Minor tweaks that look nice on a dark background
        "axes.titleweight": "bold",
        "axes.titlesize":   10,
        "axes.labelsize":   10,
        # Turn on anti‑aliasing for smoother markers
        "lines.antialiased": True,
    }

    mpl.rcParams.update(dark_style)

    # ----------------------------------------------------------------------
    # 1️⃣  Build the figure / projection
    # ----------------------------------------------------------------------
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection="aitoff")

    # ----------------------------------------------------------------------
    # 2️⃣  Convert RA/Dec → Galactic l,b (radians) and wrap longitude at 180°
    # ----------------------------------------------------------------------
    # Astropy works with Quantity objects, but we only need the numeric values.
    # The original code used `u.deg` for the units – we keep that unchanged.
    if selected_df is not None:
        ra  = selected_df["ra"] * u.deg
        dec = selected_df["dec"] * u.deg

        # Convert to Galactic coordinates (the same as your original code)
        eq = SkyCoord(selected_df["ra"].to_list(),
                    selected_df["dec"].to_list(),
                    unit=u.deg).galactic
            # scatterc , meanc = st.tabs([ 'Feature-SHAP relation', 'Mean Importance'])

        # Wrap longitude at 180° so the map stays centred (Aitoff expects -π…π)
        l = eq.l.wrap_at('180d').radian   # longitude  (radians)
        b = eq.b.radian                    # latitude   (radians)
    else: l,b = [],[]
    # ----------------------------------------------------------------------
    # 3️⃣  Plot the points – colour chosen for good contrast on black
    # ----------------------------------------------------------------------

    cmap = {
    'AGN':"#FF6F61", 'STAR': "yellow", 'YSO': "#88B04B", 'HMXB': "#F7CAC9",
    'LMXB': "#92A8D1", 'CV' : "green", 'ULX': "white", 'PULSAR': "orange"
    }
    cmap = {
    'AGN':"lightsalmon", 'STAR': "aquamarine", 'YSO': "yellow", 'HMXB': "fuchsia",
    'LMXB': "cyan", 'CV' : "deepskyblue", 'ULX': "white", 'PULSAR': "pink"
    }
    cmap = colors_dict


    marker_list = {
    'AGN':"^", 'STAR': "*", 'YSO': "^", 'HMXB': "o",
    'LMXB': "s", 'CV' : "^", 'ULX': "v", 'PULSAR': "o"
    }

    # marker_list = {
    # 'AGN':"o", 'STAR': "o", 'YSO': "o", 'HMXB': "o",
    # 'LMXB': "x", 'CV' : "x", 'ULX': "x", 'PULSAR': "x"
    # }
    size_list  = {
        'AGN': 16 , 'STAR': 24, 'YSO': 24, 'HMXB': 24,
    'LMXB': 24, 'CV' : 24, 'ULX': 24, 'PULSAR':12
    }

    class_options = [
    "AGN", "STAR", "YSO", "HMXB",
    "LMXB", "ULX", "PULSAR", "CV"
    ]
    # pdf = pd.Dataframe({'l':-1*l,'b' : b , 'c' })
    for cl in class_options:
        mask = selected_df['class 1'] == cl
        # ax.scatter(-1*l[mask], b[mask], s = point_size_scale*size_list[cl]/4, color = cmap[cl],  alpha=1, marker = marker_list[cl])
        # ax.scatter([], [], s = 100, color = cmap[cl],  alpha=1, label = cl,  marker = marker_list[cl])


        ax.scatter(-1*l[mask], b[mask], s = point_size_scale*size_list[cl]/4, facecolors = 'none', edgecolors = cmap[cl], linewidth = 1, marker = marker_list[cl])
        ax.scatter([], [], s = 42, facecolors = 'none', edgecolors = cmap[cl], linewidth = 1, label = cl, marker = marker_list[cl])

    # ----------------------------------------------------------------------
    # 4️⃣  Tweak the axes appearance
    # ----------------------------------------------------------------------
    # Turn on a light‑gray grid (visible on dark background)
    ax.grid(True, color=grid_color, linewidth=0.5, alpha=0.8)

    # Add a faint circle that marks the edge of the Aitoff projection –
    # this makes the border easier to see against the dark background.
    theta = np.linspace(-np.pi, np.pi, 360)
    ax.plot(theta, np.zeros_like(theta), color="#777777", lw=0.5, alpha=0.6,)

    # Axis labels – optional (you can comment them out if you don’t want text)
    ax.set_xlabel("Galactic longitude (deg)", color=label_color, fontsize=12, labelpad=15)
    ax.set_ylabel("Galactic latitude  (deg)", color=label_color, fontsize=12, labelpad=15)

    # # Title – also in bright colour
    # ax.set_title("Source Location (Aitoff projection)", color=point_color,
    #              fontsize=12, pad=32, )
    fig.legend(loc='upper right', ncols = 8, fontsize = 10, labelspacing = 1) 
    # ----------------------------------------------------------------------
    # 5️⃣  Restore the original rcParams before returning
    # ----------------------------------------------------------------------
    mpl.rcParams.update(old_rc)   # <-- this makes the dark‑style **local** to the function
    plt.rcParams.update({'font.size':8})
    return fig

# ----------------------------------------------------------------------
# 1️⃣ Sky map – Aitoff projection (RA/Dec)
# ----------------------------------------------------------------------
def plot_aitoff(selected_df: pd.DataFrame) -> go.Figure:
    """
    Create an Aitoff (Mollweide‑like) sky map with the selected sources.

    Parameters
    ----------
    selected_df : pd.DataFrame
        Must contain the columns ``ra`` (deg) and ``dec`` (deg).  The index
        (or a column called ``name``) will be used for the hover label.

    Returns
    -------
    plotly.graph_objects.Figure
        Interactive sky map ready for ``st.plotly_chart``.
    """
    if selected_df.empty:
        # Return an empty figure with a friendly annotation
        fig = go.Figure()
        fig.add_annotation(
            text="No sources selected – nothing to plot",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(template="simple_white")
        return fig

    # --------------------------------------------------------------
    # 1️⃣ Prepare the data – convert RA/Dec to radians and shift RA
    # --------------------------------------------------------------
    # Plotly’s Aitoff expects longitude in the range [-π, π].
    # Astronomical RA runs 0→360°, so we shift it by -180°.
    # ra_rad  = np.deg2rad(selected_df["ra"].values - 180.0)
    # dec_rad = np.deg2rad(selected_df["dec"].values)

    
    ra = selected_df["ra"]*u.deg
    dec = selected_df["dec"]*u.deg

    eq = SkyCoord(selected_df['ra'].to_list() , selected_df['dec'].to_list() , unit = u.deg).galactic 
    l  = eq.l.wrap_at('180d')
    b = eq.b

    # --------------------------------------------------------------
    # 2️⃣ Build the figure
    # --------------------------------------------------------------
    fig = go.Figure()

    # The actual scatter trace – use the index (or a column called “name”)
    # as the hover label.  If the index is not meaningful, fallback to the
    # DataFrame’s ``name`` column (if it exists).
    if "name" in selected_df.columns:
        hover_labels = selected_df["class 1"]
    else:
        hover_labels = selected_df.index.astype(str)

    fig.add_trace(
        go.Scattergeo(
            lat = l,
            lon = b,
            mode = "markers",
            marker = dict(
                size = 8,
                color = "royalblue",
                line = dict(width=0.5, color="DarkSlateGrey")
            ),
            hovertemplate = "%{customdata}<br>RA: %{lon:.2f} rad<br>Dec: %{lat:.2f} rad<extra></extra>",
            customdata = hover_labels
        )
    )

    # --------------------------------------------------------------
    # 3️⃣ Layout – set the Aitoff projection and nice styling
    # --------------------------------------------------------------
    fig.update_layout(
        title = None , 
        geo = dict(
            projection_type = "aitoff",
            showland = False,
            showcoastlines = False,
            showlakes = False,
            showrivers = False,
            bgcolor = "rgba(0,0,0,0)",
            lataxis = dict(showgrid = True, dtick = 30),
            lonaxis = dict(showgrid = True, dtick = 30)
        ),
        margin = dict(l=20, r=20, t=50, b=20),
        template = "plotly_white"
    )

    # Plotly expects lon/lat in degrees for the geo layout – we give it the
    # original values (not the radian‑shifted ones) via `geojson`.
    # However, the scatter trace already has the radian values, which
    # Plotly interprets correctly for an Aitoff projection.
    return fig


# ----------------------------------------------------------------------
# 2️⃣ Local explanation – horizontal bar chart of feature contributions
# ----------------------------------------------------------------------



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









@st.cache_data
def explain_local(source_name: str,
                  feature_df: pd.DataFrame,
                  top_n: int = 10, class_df = None) -> go.Figure:
    """
    Return a Plotly bar chart that visualises the contribution of each
    feature for a single source.

    Parameters
    ----------
    source_name : str
        The identifier of the source (must match the index of ``feature_df``).
    feature_df : pd.DataFrame
        Rows are sources, columns are feature names, values are contribution
        magnitudes (positive = supports class, negative = opposes class).
    top_n : int, default 10
        Show only the ``top_n`` features by absolute contribution.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    if source_name not in feature_df.index:
        # Graceful fallback – empty figure with a message
        fig = go.Figure()
        fig.add_annotation(
            text=f"SHAP Value not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(template="simple_white", height = 300)
        return fig

    # --------------------------------------------------------------
    # 1️⃣ Pull the row for the chosen source
    # --------------------------------------------------------------
    try:
        feature_df = feature_df.drop(columns = ['gal_b2', 'gal_l2', 'class', 'pred_prob'])
    except: pass
    row = feature_df.loc[source_name].copy()

    # --------------------------------------------------------------
    # 2️⃣ Sort by absolute value and keep the top_n
    # --------------------------------------------------------------
    sorted_abs = row.sort_values(ascending=False)
    top_features = sorted_abs.head(top_n).index
    contributions = row[top_features]

    # --------------------------------------------------------------
    # 3️⃣ Build a horizontal bar chart (positive → right, negative → left)
    # --------------------------------------------------------------
    fig = go.Figure()

    # Plotly automatically orders bars from bottom→top; we reverse the
    # order so the *most important* feature appears at the top.
    contributions = contributions[::-1]

    fig.add_trace(
        go.Bar(
            y = [ci[:-5] for ci in contributions.index],
            x = contributions.values,
            orientation = "h",
            marker = dict(
                color = np.where(contributions.values >= 0,
                                 "silver", "gray")
            ),
            hovertemplate = "%{y}<br>Contribution: %{x:.3f}<extra></extra>"
        )
    )

    # --------------------------------------------------------------
    # 3️⃣ Layout – title, axis labels, and a vertical line at 0
    # --------------------------------------------------------------
    fig.update_layout(
        title = dict(
            text = f"Class: {class_df.loc[source_name]['class 1']}",
            x = 0.5,
            xanchor = "center" , 

        ),
        xaxis = dict(
            title = "SHAP Value (Contribution in OvR classifier)",
            zeroline = True,
            zerolinewidth = 2,
            zerolinecolor = "gray"
        ),
        yaxis = dict(
            title = "Feature",
            automargin = True
        ),
        margin = dict(l=5, r=5, t=50, b=5),
        template = "plotly_white",
        # height = 300
    )
    fig.update_yaxes(showgrid=True, gridcolor = '#616161', gridwidth = 1)
    fig.update_xaxes(showgrid=True, gridcolor = '#616161', gridwidth = 1)
    return fig











# @st.cache_data
def explain_global(source_list: str,
                  feature_df: pd.DataFrame,
                  top_n: int = 20):
    if len(source_list) <3:
        # Graceful fallback – empty figure with a message
        fig = go.Figure()
        fig.add_annotation(
            text=f"SHAP Value not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(template="simple_white", height = 300)
        return fig
    try:
        feature_df = feature_df.drop(columns = ['gal_b2', 'gal_l2', 'class', 'pred_prob'])
    except: pass
    feature_df = feature_df.loc[source_list].copy()
    row = feature_df.mean(axis=0).sort_values(ascending=False)

    sorted_abs = row.sort_values(ascending=False)
    top_features = sorted_abs.head(top_n).index
    contributions = row[top_features]

    # --------------------------------------------------------------
    # 3️⃣ Build a horizontal bar chart (positive → right, negative → left)
    # --------------------------------------------------------------
    fig = go.Figure()

    # Plotly automatically orders bars from bottom→top; we reverse the
    # order so the *most important* feature appears at the top.
    contributions = contributions[::-1]

    fig.add_trace(
        go.Bar(
            y = [ci[:-5] for ci in contributions.index],
            x = contributions.values,
            orientation = "h",
            marker = dict(
                color = np.where(contributions.values >= 0,
                                 "silver", "crimson")
            ),
            hovertemplate = "%{y}<br>Contribution: %{x:.3f}<extra></extra>"
        )
    )

    # --------------------------------------------------------------
    # 3️⃣ Layout – title, axis labels, and a vertical line at 0
    # --------------------------------------------------------------
    fig.update_layout(
        title = dict(
            text = f"Mean Feature contributions for {len(feature_df)} Sources",
            x = 0.5,
            xanchor = "center"
        ),
        xaxis = dict(
            title = "SHAP Value (contribution in OvR classification)",
            zeroline = True,
            zerolinewidth = 2,
            zerolinecolor = "gray"
        ),
        yaxis = dict(
            title = "Feature",
            automargin = True
        ),
        margin = dict(l=5, r=5, t=50, b=5),
        template = "plotly_dark",
        # height = 300
    )
    fig.update_yaxes(showgrid=True, gridcolor = '#616161', gridwidth = 1)
    fig.update_xaxes(showgrid=True, gridcolor = '#616161', gridwidth = 1)

    return fig

# 'AGN':"#FF6F61", 'STAR': "yellow", 'YSO': "#88B04B", 'HMXB': "#F7CAC9",

@st.cache_resource
def plot_shap_feat(fname , selected_sources , feat_df , feat_imp_df):
    selected_names = selected_sources.index.to_list()
    class_list = selected_sources['class 1']

    class_series = selected_sources['class 1']

    # if class_palette is None:
    # class_palette = {
    #     'AGN' : '#FF6F61',
    #     'STAR': '#1f77b4',
    #     'YSO' : 'aquamarine'
    # }

    colour_list = [colors_dict.get(cls, 'gray') for cls in class_series]

    trace = go.Scatter(
        x = feat_df.loc[selected_names][fname] , 
        y = feat_imp_df.loc[selected_names][f'{fname}_shap'] , 
        mode = 'markers' , 
        marker = dict(
            color = colour_list,  
            size = 2
        ),
        text = [f'{fname}'],
        customdata = feat_df.loc[selected_names].reset_index()[['name']], 
        hovertemplate = "%{customdata[0]}<extra></extra>"
    )
    fig = go.Figure(data = [trace])
    fig.update_layout(
    
        font = dict(size=20),
        xaxis = dict(
            title = "Feature Value",
            zeroline = True,
            zerolinewidth = 1,
            zerolinecolor = "teal", 
            # size = 14
        ),
        yaxis = dict(
            title = "Feature SHAP",
            automargin = True, 
            zeroline = True,
            zerolinewidth = 1,
            zerolinecolor = "whitesmoke"
        ),
        # margin = dict(l=100, r=20, t=60, b=40),
        template = "plotly_white",
        # xaxis_tick
        # height = 300
    )
    fig.update_yaxes(showgrid=True, gridcolor = '#616161', gridwidth = 1)
    fig.update_xaxes(showgrid=True, gridcolor = '#616161', gridwidth = 1)

    legend_traces = []
    for cls, col in class_palette.items():
        legend_traces.append(
            go.Scatter(
                x=[None], y=[None],
                mode='markers',
                marker=dict(color=col, size=8),
                name=cls,
                showlegend=False,
                # title = None
            )
        )
    for lt in legend_traces:
        fig.add_trace(lt)
    fig.update_layout(
        legend_title_text='class'      # ← sets the legend header
    )
    return fig


import seaborn as sns
@st.cache_resource
def plot_shap_feat_mpl(fname , selected_sources , feat_df , feat_imp_df, figsize = (8, 4.5)):
    selected_names = selected_sources.index.to_list()
    plt.style.use('dark_background')
    plt.rcParams.update({'font.size':8})
    pltdf = pd.DataFrame(
            {'Feature Value' :feat_df.loc[selected_names][fname] ,
            'Feature SHAP'   : feat_imp_df.loc[selected_names][f'{fname}_shap'], 
            'Class' : selected_sources['class 1']
            }
        )
    colors = [colors_dict['AGN'], colors_dict['STAR'], colors_dict['YSO']]
    # colors = [colors_dict.get(cls, 'gray') for cls in class_series]

    if(len(selected_names)>1000): s = 2
    else: s = 20
    fig, ax = plt.subplots(nrows = 1,ncols = 1,figsize = figsize)
    sns.scatterplot(data=pltdf, x='Feature Value', y='Feature SHAP', hue='Class', palette=colors, s = s, ax = ax, legend=False, hue_order = ['AGN', 'STAR', 'YSO'])
    ax.scatter([],[], s = 40 , c = colors_dict['AGN'], label = 'AGN' )
    ax.scatter([],[], s = 40 , c = colors_dict['STAR'] , label = 'STAR')
    ax.scatter([],[], s = 40 , c = colors_dict['YSO'] , label = 'YSO')
    sns.despine()
    # plt.grid(True, color='gray', ls=  '--', lw = 0.2)
    plt.grid(False)
    ax.set_xlabel(f'{fname} Value')
    ax.set_ylabel(f'{fname} SHAP value (contribution)')
    ax.legend(loc=1)
    ax.axhline(y=0, ls = '--', c = 'white', lw =1)
    return fig