"""
Reusable Streamlit Components
Custom UI components for consistent design across the application
"""

import streamlit as st
import pandas as pd


class ContentSections:
    """Class to store project markdown content sections"""
    
    @staticmethod
    def get_home_content(project_title, project_description):
        """Generate home page content"""
        return f"""
        ### 🎯 **Project Overview**
        
        {project_description}
        
        ---
        
        #### 🔍 **Key Features**
        ✅ **Advanced Data Preprocessing** – Clean, transform, and prepare data for ML models  
        ✅ **Multiple ML Algorithms** – Train and compare various models automatically  
        ✅ **Interactive Predictions** – Single and batch prediction capabilities  
        ✅ **Comprehensive Analytics** – Detailed performance metrics and visualizations  
        ✅ **User-Friendly Interface** – Intuitive Streamlit-based web application  
        
        ---
        
        #### 🛠️ **Technologies Used**
        🔹 **Python** – Core programming language  
        🔹 **Streamlit** – Interactive web application framework  
        🔹 **Scikit-learn** – Machine learning algorithms  
        🔹 **Pandas & NumPy** – Data manipulation and analysis  
        🔹 **Plotly & Matplotlib** – Advanced visualizations  
        """
    
    @staticmethod
    def get_about_content(paper_title, authors, publication):
        """Generate about page content"""
        return f"""
        ### 📚 **Base Paper**
        
        **Title:** {paper_title}  
        **Authors:** {authors}  
        **Published:** {publication}  
        
        ---
        
        #### 🎯 **Research Objective**
        This project implements the methodology proposed in the base paper, focusing on:
        
        ✅ Accurate prediction using state-of-the-art ML techniques  
        ✅ Comprehensive data preprocessing and feature engineering  
        ✅ Model comparison and performance evaluation  
        ✅ Real-world application and deployment  
        
        ---
        
        #### 🔬 **Methodology**
        The implementation follows a systematic approach:
        
        1️⃣ **Data Collection & Preprocessing**  
        2️⃣ **Feature Engineering & Selection**  
        3️⃣ **Model Training & Optimization**  
        4️⃣ **Evaluation & Validation**  
        5️⃣ **Deployment & Testing**  
        """


class DataTable:
    """Enhanced data table component with styling"""
    
    def __init__(self, df, height=400):
        """
        Initialize data table
        
        Args:
            df: Pandas DataFrame to display
            height: Table height in pixels
        """
        self.df = df
        self.height = height
    
    def display_table(self):
        """Display styled data table"""
        st.dataframe(
            self.df,
            use_container_width=True,
            height=self.height
        )
        
        st.caption(f"📊 Showing {len(self.df)} rows × {len(self.df.columns)} columns")


class MetricCard:
    """Custom metric card component"""
    
    @staticmethod
    def display(label, value, delta=None, icon="📊"):
        """
        Display a styled metric card
        
        Args:
            label: Metric label
            value: Metric value
            delta: Change value (optional)
            icon: Emoji icon
        """
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"<h1 style='text-align: center;'>{icon}</h1>", unsafe_allow_html=True)
        with col2:
            st.metric(label=label, value=value, delta=delta)


class InfoBox:
    """Styled information boxes"""
    
    @staticmethod
    def success(message):
        """Display success message"""
        st.markdown(
            f'<div class="success-box">✅ {message}</div>',
            unsafe_allow_html=True
        )
    
    @staticmethod
    def info(message):
        """Display info message"""
        st.markdown(
            f'<div class="info-box">ℹ️ {message}</div>',
            unsafe_allow_html=True
        )
    
    @staticmethod
    def warning(message):
        """Display warning message"""
        st.warning(f"⚠️ {message}")
    
    @staticmethod
    def error(message):
        """Display error message"""
        st.error(f"❌ {message}")


class ProgressTracker:
    """Track and display progress through pipeline steps"""
    
    def __init__(self, steps):
        """
        Initialize progress tracker
        
        Args:
            steps: List of step names
        """
        self.steps = steps
        self.current_step = 0
    
    def display(self, current_step_index):
        """Display progress bar"""
        progress = (current_step_index + 1) / len(self.steps)
        st.progress(progress)
        st.caption(f"Step {current_step_index + 1}/{len(self.steps)}: {self.steps[current_step_index]}")


def create_sidebar_navigation(pages):
    """
    Create sidebar navigation with styled buttons
    
    Args:
        pages: List of page names
    
    Returns:
        Selected page name
    """
    st.sidebar.markdown(
        '<div class="sidebar-title">📋 Navigation</div>',
        unsafe_allow_html=True
    )
    
    if "page" not in st.session_state:
        st.session_state["page"] = pages[0]
    
    for page in pages:
        if st.sidebar.button(page, key=f"btn_{page}"):
            st.session_state["page"] = page
    
    return st.session_state["page"]


def display_feature_card(title, description, icon="🔹"):
    """
    Display a feature card
    
    Args:
        title: Card title
        description: Card description
        icon: Emoji icon
    """
    st.markdown(
        f"""
        <div class="feature-card">
            <h3>{icon} {title}</h3>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
