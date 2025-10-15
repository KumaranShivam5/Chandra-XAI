
import streamlit as st
import pandas as pd
from utils import data_loader, filtering, visualisation
from streamlit import column_config

import json

st.set_page_config(page_title="Chandra XAI", layout="wide",)
st.set_page_config(layout="wide")
# --------------------------------------------------------------
# Load data (cached)
# --------------------------------------------------------------
@st.cache_data
def load_data():
    cls_df = data_loader.load_classification()
    feat_df = data_loader.load_feature_contributions()
    val_df = data_loader.load_feature_value()
    return cls_df, feat_df , val_df

@st.cache_data
def download_df(df):
    return df.to_csv().encode("utf-8")

from introduction.background import intro_page
if "initialized" not in st.session_state:
    intro_page(what_to_show=['intro', 'how-to-use', 'desc', 'ref'])
    st.session_state.initialized = True


# @st.dialog("Explainable Classification of CSC Sources", width='large')
# def intro_dialog():
#     with open('./introduction/background.txt', 'r') as f:
#         content = f.read()
#     st.write(content)



# intro_page(what_to_show=['intro', 'how-to-use', 'desc'])

classification_df, feature_df , val_df = load_data()

# --------------------------------------------------------------
# Sidebar – filter controls (unchanged)
# --------------------------------------------------------------
# st.sidebar.title("Chandra Source Classification")

st.sidebar.header("Filter Sources")

st.markdown("""
        <style>
        /* Example: Reduce top padding of the main content block */

        .stSidebarHeader{
            margin-bottom : 0 !important; 
            height:0 !important;
        }

        
        </style>
    """, unsafe_allow_html=True)


cmp_filter_container =st.sidebar.expander("CMP Threshold : ", expanded=True)

cmp_thresh = cmp_filter_container.slider(
    "CMP", 0.5, 1.0, 0.8, 0.01
)
cmp_filter_container.caption("Filter Sources with Class Membership Probability > selected CMP")
# st.sidebar.divider()
class_options = [
    "AGN", "STAR", "YSO", "HMXB",
    "LMXB", "ULX", "PULSAR", "CV"
]

class_expander = st.sidebar.expander('Select Classes', expanded = True)
# select_all = class_expander.checkbox('All Classes', True)
# selected_classes = [
#     c for c in class_options if class_expander.checkbox(c, True)
# ]

# st.write(selected_classes)

# options = ["North", "East", "South", "West"]
selected_classes = class_expander.pills("class", class_options, selection_mode="multi", label_visibility ='collapsed', )
class_expander.caption('Filter sources based on these selected classes')
# if class_expander.toggle('Select All'):
#     selected_classes = class_options
# else:
#     selected_classes = selected_classes_pil

cone_expander = st.sidebar.expander('Cone Search')

ra_input = cone_expander.number_input("RA (deg)", 0.0, 360.0, 0.0, 0.1)
dec_input = cone_expander.number_input("Dec (deg)", -90.0, 90.0, 0.0, 0.1)
radius = cone_expander.number_input("Search radius (arcmin)", 0.0, 180.0, 0.0, 0.1)

# st.sidebar.divider()
shap_filter = st.sidebar.expander("SHAP Filter", expanded=True)
# st.sidebar.subheader('SHAP Analysis')
with_shap = shap_filter.toggle('Turn ON toggle for selecting only those sources where SHAP exlpanation is available', False)
# st.sidebar.caption('Turn ON toggle for selecting with SHAP exlpanation available')

SEED = 42
default_sample = classification_df.sample(100, random_state = SEED)
st.session_state.setdefault("filtered_df", default_sample)
st.session_state["selected_rows"] = default_sample
cmap = {
 'AGN':"lightsalmon", 'STAR': "#6ac7ff", 'YSO': "yellow", 'HMXB': "fuchsia",
'LMXB': "cyan", 'CV' : "aquamarine", 'ULX': "white", 'PULSAR': "pink"
}

if st.sidebar.button("Submit", type = 'primary', use_container_width=True,):
    # Apply filters once and store in session state
    filtered = filtering.apply_filters(
        df=classification_df,
        cmp_thresh=cmp_thresh,
        ra=ra_input if radius > 0 else None,
        dec=dec_input if radius > 0 else None,
        radius=radius,
        classes=selected_classes,
        with_shap = with_shap
    )
    st.session_state["filtered_df"] = filtered
else:
    # first run – show the whole (unfiltered) table
     # first run – show the whole (unfiltered) table
    st.session_state.setdefault("filtered_df", default_sample)
    st.session_state["selected_rows"] = default_sample


# --------------------------------------------------------------
# 2 × 2 layout
# --------------------------------------------------------------

st.markdown("""
        <style>
        /* Example: Reduce top padding of the main content block */
        .block-container {
            padding-top: 1rem; /* Adjust as needed */
        }
        .stMainBlockContainer{
            padding-left: 1rem !important;
            padding-right : 1rem !important;
            padding-top:2rem !important;
            }
        .stAppHeader{
        
            }
        .stSidebarHeader{
            margin-bottom : 0 !important; 
            height:0 !important;
        }
        /* Example: Reduce gap between elements in a specific column */
        [data-testid="column"]:nth-of-type(1) [data-testid="stVerticalBlock"] {
            gap: 0rem; /* Remove gap */
        }
        
        </style>
    """, unsafe_allow_html=True)


# st.title('Probabilistic Classification Of __Chandra__ Sources')


main_area = st.container()
left_col, right_col = main_area.columns([0.6, 0.4], gap = 'small', border = False)
data_col = left_col.container(border = True)

with data_col:
    st.header("Probabilistic Classification of __Chandra__ Sources")
    details, download_btn_col = st.columns([0.6,0.4], border=True,)
    details.write("Classification table for Point sources in the Chandra Source Catalogue-2.0. The class and the class membership probability is given for highest probable class and second highest probable class.")
    info = details.empty()
    info.info('Currently showing randomly 1001 randomly selected sources. Use sidebar "filter" to search the entire catalogue')
    st.markdown(
        """
        <style>
        .stDataEditor {height: calc(100vh - 180px) !important;}
        .stDataFrame {height: calc(80vh - 180px) !important;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    df_for_editor = st.session_state["filtered_df"].reset_index()
    current_df = st.session_state["filtered_df"]
    data_selection = st.dataframe(current_df.reset_index(), selection_mode = "multi-row", on_select = "rerun", height = 700, hide_index = True)
    selected_rows = current_df.iloc[data_selection.selection.rows]
    # st.session_state["selected_rows"] = selected_rows
    selected_idx = data_selection.selection.rows
    if not selected_idx:                      # ← empty list → select all rows
        selected_idx = list(range(len(current_df)))   # all row positions

    selected_rows = current_df.iloc[selected_idx]
    st.session_state["selected_rows"] = selected_rows

    # --------------------------------------------------------------
    # 2️⃣ “Details” button – tells the right‑hand panels to refresh
    # --------------------------------------------------------------
    # download_btn_col.write(f'Current table : {len(selected_rows)} Sources')
    info.success(f"Displayed Sources  : {len(current_df)} | Selected sources : {len(selected_rows)}")
    download_btn_col.write('Download')
    button_cols = download_btn_col.container()

    button_cols.download_button('All', download_df(current_df), file_name = 'csc-classification.csv', use_container_width=True, icon = ":material/download:")
    button_cols.download_button('Selected', download_df(selected_rows), file_name = 'csc-classification-selected.csv', use_container_width=True, icon = ":material/download:", type='primary')
    footer = st.container()
    fbtn1, fbtn2, fbtn3 , fbtn4 = footer.columns([1,1,1,1])
    if fbtn1.button("About", width='stretch') : intro_page(what_to_show=['intro'])
    if fbtn2.button("How to Use", width='stretch') : intro_page(what_to_show=['how-to-use'])
    if fbtn3.button("Table Desc.", width='stretch') : intro_page(what_to_show=['desc'])
    if fbtn4.button("References", width='stretch') : intro_page(what_to_show=['ref'])
    footer.markdown('''
        * **Classification Paper** : Kumaran et al. 'Automated classification of Chandra X-ray point sources using machine learning methods.' MNRAS 520.4 (2023): 5065-5076.
        * **SHAP analysis Paper** : Kumaran et al. 'Explainable machine learning classification of Chandra X-ray sources: SHAP analysis of multi-wavelength features.' ApJ, Under review.
        
        ''')

# --------------------------------------------------------------
# Right side – sky map (top) & explanation (bottom)
# --------------------------------------------------------------
with right_col:
    # sky_container = st.container(border = True, height=200)
    sky_container = st.columns(1,border=True)

    expl_container = st.container(border = False)

   

    # explanation – dropdown limited to the selected sources
    local_ex_tab , global_ex_tab = expl_container.tabs(['**Local SHAP Explanation**', '**Global SHAP Analysis**'])
    # local_ex_tab , global_ex_tab = expl_container.columns([0.45,0.55], border =True , gap='small')
    # local_ex_tab = expl_container.container(border = True)
    # global_ex_tab = expl_container.container(border = True)

    if not st.session_state["selected_rows"].empty:
        with local_ex_tab:
            
            
            # st.write("**Local explanation**")

            src_name = st.selectbox(
                "Choose a source",
                options = st.session_state["selected_rows"].index.to_numpy()[st.session_state["selected_rows"]['SHAP']=='✓'],
                key="explanation_selector",
            )
            expl_fig = visualisation.explain_local(src_name, feature_df, top_n  = 12, class_df = st.session_state["selected_rows"])
            # st.write(st.session_state["selected_rows"].loc[src_name])
            st.plotly_chart(expl_fig, use_container_width=True, theme="streamlit")
        
        with global_ex_tab:
            # st.write("**Global SHAP Analysis**")
            if(len(st.session_state["selected_rows"])<=10):
                st.info("Select more than 10 sources for Global explanation")
            else:
                # st.caption('Global SHAP Analysis. Using the Aggregate of local explanation, mean of Local importances and overall SHAP-feature correlation is visualised')
                # meanc , scatterc = global_ex_tab.tabs(['Mean Importance', 'Feature-SHAP relation'])
                # scatterc , meanc = st.tabs([ 'Feature-SHAP relation', 'Mean Importance'])
                
                scatterc = global_ex_tab.container()
                # scatterc = global_ex_tab.expander('Feature-SHAP relation')
                # meanc = global_ex_tab.expander('Mean Importance')

                global_fig = visualisation.explain_global(st.session_state["selected_rows"][st.session_state["selected_rows"]['SHAP']=='✓'].index.to_list() , feature_df, top_n = 12)
                # meanc.plotly_chart(global_fig, use_container_width=True, theme="streamlit")

                # with scatterc:
                fname = scatterc.selectbox('Select Feature', options = val_df.columns.to_list())
                selected_names = st.session_state["selected_rows"][st.session_state["selected_rows"]['SHAP']=='✓']
                scatter_fig = visualisation.plot_shap_feat_mpl(fname = fname , selected_sources = selected_names ,  feat_df = val_df , feat_imp_df = feature_df , figsize = (5,3) )
                # scatterc.plotly_chart(scatter_fig , use_container_width=True, theme="streamlit")
                scatterc.pyplot(scatter_fig , use_container_width=True, )


    else:
        local_ex_tab.info("Select a source with **SHAP ✅** in the __classification table__ for local explanation")
        global_ex_tab.info("Select more than 10 sources for Global explanation")

 
    # with sky_container:
        # mpl  = st.tabs(['Source Location', 'Aladin Map'])
        # mpl  = st.container()
    if not st.session_state["selected_rows"].empty:
            # with mpl:
            # point_size = st.slider()
            # st.write('plotting sources on aitoffsdsd')
            # plot_container = st.container()
            # point_scale = mpl.expander(label = 'Configure Plot').slider("Scatter Point Size", 1, 20, 4, 1)
        point_scale = 1
        fig_map = visualisation.plot_aitoff_mpl_dark(st.session_state["selected_rows"], point_size_scale = point_scale)
        sky_container[0].pyplot(fig_map, width = "stretch")
            # with aladin:
            #df = st.session_state["selected_rows"].rename(columns={'class 1' : 'class'})
            #df_to_plot = df.to_dict(orient='records')
            #with open('aladin_lite.html', 'r') as f:
                # st.write(df_to_plot)
            #    html_code = f.read().replace('DATA_PLACEHOLDER', json.dumps(df_to_plot))
            #    with aladin: 
            #        legend_html = ''
            #        st.spinner('Loading Sources')
            #        for c in class_options:
            #            legend_html+= f"<div style='display:flex;width:100%;align-items: center;justify-content: center;'><span style = 'font-weight:bold;color:{cmap[c]}'> {c}</span></div>"
            #        legend_html = f"<div style = 'display:flex; align-items:center;justify-content:space-evenly;font-family:Sans-Serif;font-size:0.8rem;'>{legend_html}</div>"
            #        st.components.v1.html(legend_html, height = 20)
            #        st.components.v1.html(html_code,height = 450)
    else:
        # mpl.info("Select at least one source from the table to plot on sky map")err
        # aladin.info("Select at least one source from the table to to view on Aladin Sky map")
        sky_container[0].info("Select at least one source from the table to plot on sky map")

