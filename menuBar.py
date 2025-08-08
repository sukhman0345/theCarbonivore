import streamlit as st
from streamlit_option_menu import option_menu
from about import show_about
from visualization import show_visualization
from touch import get_in_touch
from  preprocessing import show_preprocessing

def main_app():
    # Check if user is logged in
    if 'user' not in st.session_state:
        st.warning("Please sign in to continue...")
        st.stop()
     
    # Sidebar logout and user display
    st.sidebar.markdown("## 🌿 The Carbonivore")

    st.sidebar.markdown("---")
    st.sidebar.write(f"👤 {st.session_state['user']['email']}")

    if st.sidebar.button("🚪Logout"):
        st.session_state.pop("user", None)
        st.success("You have been logged out.")
        st.rerun()

    # Horizontal menu
    selected = option_menu(
        menu_title="The Carbonivore",
        options=["About","Pre-Processing","Visualization", "Get In Touch"],
        icons=["house","funnel", "search", "patch-question-fill"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    # Page Content Based on Selection
    if selected == "About":
        show_about()
    elif selected == "Pre-Processing":
         show_preprocessing()    
    elif selected == "Visualization":
        show_visualization()
    elif selected == "Get In Touch":
        get_in_touch()
        
