import streamlit as st

# --------------------------------------------------------------
# Page configuration (run once at the top of the script)
# --------------------------------------------------------------
# @st.cache_data
@st.dialog("Explainable Classification of CSC Sources", width='large')
def intro_page(what_to_show = ['intro', 'how-to-use','desc','links','References', 'Citation']):
    # --------------------------------------------------------------
    # 1️⃣  Scientific background
    # --------------------------------------------------------------
    if 'intro' in what_to_show:
        # st.header("About the Portal : Chandra XAI")
        st.markdown(
            """
            # `Background`
            The *Chandra* X-ray Observatory has accumulated more than a million detections
            over two decades, spanning a mixture of **stellar coronal emitters, 
            active galactic nuclei (AGN), and compact objects** (X-ray binaries,
            pulsars, cataclysmic variables).  

            The Chandra Source Catalogue$^1$ contains about 300,000 X-ray point sources. The nature of majority of them is not unconfirmed. In **Kumaran et.al 2023** we used LightGBM decision tree based model to clasify 277,069 objects into 8 class of X-ray emitting sources : Active Galactic Nuclei (AGN), Young Stellar Object (YSO), X-ray emitting Stars (STAR), High Mass X-ray Binary (HMXB), Low Mass X-ray Binary (LMXB), Cataclysmic Variable (CV), Ultra-luminuous X-ray Sources (ULX), Pulsar (PULSAR). For classification we use 41 multiwavelength features (see Table 2 of **Kumaran et.al 2023* for the details of these features).
        
            * Out of the selected 277069 point sources in the CSC-2.0, we identified the class of 7703 objects using the published literature.
            * We trained a LightGBM model to assign class membership probabilities to remaining 269366 sources with unknown class.
            * This protal presents the classification table of 269366 sources including 54,770 robustly classified sources (over $3\sigma$ significance)$^2$ and 14,066 sources at $>4\sigma$ significance$^2$.
            
            # `SHAP Analysis`
            For investingating the multiwavelength properties curical for class-wise identification of these objects, we applied SHAP analysis, an Explainable-AI technique for the majority classes : AGN, Star and YSO. Using SHAP analysis, we obtain local explanation of individual sources and their feature dependency. The paper **Kumaran et.al. (under review)** discuss the analysis in detail. 

            """
        )
    if 'desc' in what_to_show:
        with st.expander("# Classification table description : ", expanded = True):
            st.markdown(
                """
                    *    Column 1: Name : (Observation ID of the source in the CSC-2.0)
                    *    Column 2: ra (J2000) in deg
                    *    Column 3: dec (J2000) in deg
                    *    Column 4: class 1: Predicted class with highest CMP
                    *    Column 5: CMP1: probability for highest probable class
                    *    Column 6: class 2: Predicted class with second highest CMP
                    *    Column 7: CMP2: probability of second highest class.
                    *    Column 8 : SHAP : '✓' sign indicates, that SHAP analysis is available for this sources
            """)
    if 'how-to-use' in what_to_show:
        with st.expander("# How to use the portal : ", expanded = True):
            st.markdown(
                """
                1. When the portal first loads, it 100 sources selected at random from the catalog of 269366 sources.
                2. Use the sidebar to obtain catalogue of all sources based on the following **filters**: 
                """
            )
            f1,f2,f3,f4 = st.columns([1,1,1,2,], border=True)
            f1.markdown("""
            #### CMP Threshold : 
            Use the slider to adjust the CMP threshold.
            """)
            f2.markdown("""
            #### Classes : 
            Select the classes to be included in the result.
            """)
            f3.markdown("""
            #### Cone Search : 
            Enter RA, DEC and the search radius
            """)
            f4.markdown("""
            #### SHAP filter : 
            SHAP analysis is done only for high-confident sources belonging to the majority classes: AGN, YSO and STAR. Turnging on this toggle will filter only those sources where SHAP analysis is available.
            """)
            st.markdown(
                """
                3. After setting these filture press the `SUBMIT` button to obtain the filtered data-table.
                4. Based on the filter, the classifiction table is loaded in the central panel.
                5. When the table loads, all the sources are selected by default.
                6. Select a subset of sources using the checkbox (first un-named column).
                7. For selected sources, the sky location are shown in the top-right corner.
                8. In the Local explanation tab, select individual sources from the down (only those sources appear in the drop-down for which SHAP value is available) to get the feature importance for that particular source.
                9. In the Global Explanation tab, the feature-SHAP relation scatter plot is shown for the selected sources.
                """
            )
        with st.expander("# Illustration : Reproducing _Fig 5._ and _Fig. 7_ from the paper **Kumaran et.al (under review)**"):
            st.markdown(
                """
                1. Sidebar filters: 
                 * Set the CMP threshold to 0.97
                 * Select only "AGN"
                 * Leave the 'Cone Search' filter blank
                 * Turn ON the SHAP toggle
                2. Preshh `Submit` button
                3. After table loads, Use top-left corner in the table to select all the rows.
                4. In the Local Explanation tab (bottom right panel) click the drop down
                5. Select the source '2CXO J01422.8-005331' from the drop-down or type this source ID, it will give the local explanation of this source as in the _Fig.5_
                6. Go to 'Global Explanation tab'
                7. Under the drop-down,select 'W1' feature. This will generate the 1st panel of AGN row in the Fig 5.
                8. Similarly other features can be selected from the drop-down
                9. For other class, in step 1, select 'Star' or 'YSO' to reproduce next two rows.
                10. Use these filters, by selecting multiple classes to see the SHAP feature plots for all possible combinations of classes and features.
                11. As an illustration, select all three AGN, STAR and YSO and see the comparison of global SHAP-feature plot.
                
                _note : Due to difference in scatter-point size and opacity the  plot in the portal will not be exactly identical as the paper._
                """
            )
        with st.expander("Additional Plots : SHAP-feature plots for top 12 features"):
            i1,i2,i3 = st.columns([1,1,1], border=False)
            i1.image('images/AGN-shap-feat.png', width='content')
            i2.image('images/YSO-shap-feat.png', width='content')
            i3.image('images/STAR-shap-feat.png', width='content')

    # # --------------------------------------------------------------
    # # 5️⃣  How to use the portal (step-by-step)
    # # --------------------------------------------------------------
    # st.header("  How to use the portal")
    # with st.expander(" Step-by-step guide (click to expand)"):
    #     st.markdown(
    #         """
    #         1. **Select a module** from the left-hand navigation bar – *Data*, *Classification*,
    #         *SHAP*, or *Download*.  
    #         2. **Apply filters** (sky region, flux range, observation ID, etc.) using the
    #         sidebar widgets; the main table updates automatically.  
    #         3. **Inspect a source** – click a row to open a modal that displays:  
    #         - The complete feature vector.  
    #         - A bar chart of the four class probabilities.  
    #         - A SHAP waterfall diagram indicating which features push the prediction
    #             toward each class.  
    #         4. **Generate custom visualisations**: choose X- and Y-axes from the feature list,
    #         optionally colour-code points by the dominant SHAP contribution, and download
    #         the figure (PNG/SVG).  
    #         5. **Export results**: the *Download* tab allows you to export the current
    #         selection as CSV or JSON; a short Python snippet for the REST API
    #         (`/api/v1/query?...`) is provided for scripted access.  
    #         6. **Re-run the classifier** (optional): upload a plain-text list of source IDs
    #         (≤ 10 000).  The portal returns a new probability table together with the
    #         corresponding SHAP values.  

    #         **Tip:** Use the search bar (top-right) to locate a source by its *Chandra* ID or
    #         by coordinates; the table scrolls to the matching entry instantly.  
    #         """
    #     )

    # --------------------------------------------------------------
    # 6️⃣  Acknowledgements
    # --------------------------------------------------------------
        # st.header(" Acknowledgements")
        # st.markdown(
        #     """
        #     • The *Chandra* X-ray Center (CXC) for the archival data and the High-Energy
        #     Astrophysics Science Archive Research Center (HEASARC) for the ancillary
        #     multi-wavelength catalogues.  

        #     • This portal was built with **Streamlit**, **scikit-learn**, **XGBoost**, **SHAP**, and
        #     **Astropy**, all of which are open-source tools that underpin modern astronomical
        #     data analysis.  

        #     • We thank the anonymous referee for insightful comments that improved both the
        #     manuscript and the web interface.  
        #     """
        # )

    # --------------------------------------------------------------
    # 7️⃣  References (academic citation style)
    # --------------------------------------------------------------
    if 'ref' in what_to_show:
        st.header("  References")
        st.markdown(
            """
            1. **Classification Paper** : Kumaran et al. 'Automated classification of Chandra X-ray point sources using machine learning methods.' MNRAS 520.4 (2023): 5065-5076.
            2. **SHAP analysis Paper** : Kumaran et al. 'Explainable machine learning classification of Chandra X-ray sources: SHAP analysis of multi-wavelength features.' ApJ, Under review.
            3. **Chandra Source Catalogue-2.0**: Evans, Ian N., et al. "The chandra source catalog." The Astrophysical Journal Supplement Series 189.1 (2010): 37.
            4. SHAP Analysis : 
                * Lundberg, Scott M., et al. "From local explanations to global understanding with explainable AI for trees." Nature machine intelligence 2.1 (2020): 56-67.
                * SHAP python package : https://shap.readthedocs.io/en/latest/
            5. Astropy Collaboration (2018). Price-Whelan, Adrian M., et al. "The astropy project: Building an open-science project and status of the v2. 0 core package." The Astronomical Journal 156.3 (2018): 123.
            6. Portal developed using Streamlit framework. *Streamlit Documentation*. https://docs.streamlit.io  

            """
        )

    # --------------------------------------------------------------
    # Footer (tiny caption)
    # --------------------------------------------------------------
    st.markdown("---")
    st.caption(
      "Kumaran et al., MNRAS 520.4 (2023): 5065-5076. |  Kumaran et al. ApJ, Under review."
    )
    # st.caption(
    #   "Kumaran et al. 'Automated classification of Chandra X-ray point sources using machine learning methods.' MNRAS 520.4 (2023): 5065-5076."
    # )
    # st.caption(
    #   "Kumaran et al. 'Explainable machine learning classification of Chandra X-ray sources: SHAP analysis of multi-wavelength features.' ApJ, Under review."
    # )