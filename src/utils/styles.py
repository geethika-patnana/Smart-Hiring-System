"""
Custom CSS Styles for Streamlit Application
Provides gradient titles, styled buttons, and enhanced UI components
"""

TITLE_STYLE = """
<style>
    .styled-title {
        font-family: 'Arial', sans-serif;
        font-size: 48px;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 10px;
        margin-bottom: 20px;
    }
    
    .subtitle {
        font-family: 'Arial', sans-serif;
        font-size: 20px;
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }
</style>
"""

SIDEBAR_STYLE = """
<style>
    /* Sidebar title styling */
    .sidebar-title {
        font-family: 'Arial', sans-serif;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        margin-bottom: 20px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Sidebar button styling */
    .stButton>button {
        width: 100%;
        text-align: center;
        padding: 12px;
        margin: 5px 0;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        border: none;
        transition: 0.3s;
    }

    /* Hover effect for buttons */
    .stButton>button:hover {
        background: linear-gradient(90deg, #764ba2, #667eea);
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    /* Download button styling */
    .stDownloadButton>button {
        width: 100%;
        text-align: center;
        padding: 12px;
        margin: 5px 0;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        background: linear-gradient(90deg, #11998e, #38ef7d);
        color: white;
        border: none;
        transition: 0.3s;
    }

    /* Hover effect for download button */
    .stDownloadButton>button:hover {
        background: linear-gradient(90deg, #38ef7d, #11998e);
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(56, 239, 125, 0.4);
    }
    
    /* Metric cards styling */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 15px;
        border-radius: 8px;
        color: white;
        margin: 10px 0;
    }
    
    /* Success boxes */
    .success-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 15px;
        border-radius: 8px;
        color: white;
        margin: 10px 0;
    }
</style>
"""

CARD_STYLE = """
<style>
    .feature-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    
    .feature-card h3 {
        color: #667eea;
        margin-bottom: 10px;
    }
    
    .feature-card p {
        color: #666;
        line-height: 1.6;
    }
</style>
"""

def apply_custom_styles():
    """Apply all custom styles to the Streamlit app"""
    import streamlit as st
    st.markdown(TITLE_STYLE, unsafe_allow_html=True)
    st.markdown(SIDEBAR_STYLE, unsafe_allow_html=True)
    st.markdown(CARD_STYLE, unsafe_allow_html=True)
