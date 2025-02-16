import streamlit as st
import time

# Ensure this is the first Streamlit command
st.set_page_config(page_title="Face Detection Song Recommender", layout="centered")

def Home():
    # Display title with improved wording
    st.title(" Face Detection Song Recommender")

    # Add an image with an appropriate caption
    #st.image("jay.jpeg", use_column_width=True, caption="AI-powered Song Recommendations")

    # Welcome message with a divider for better structure
    st.markdown("---")
    st.header("Welcome to Your Personalized Music Experience!")
    st.subheader("Discover songs based on your mood with AI-driven recommendations.")

    # Simulating loading effect for better UX
    with st.spinner("Loading features..."):
        time.sleep(1.5)

    # Display a call-to-action message
    st.success(" Start by uploading your image and let AI do the magic!")

    # Footer with branding
    st.markdown("---")
    st.markdown(
        """
        **Made with  by 909_jayhind**  
         [Follow us on Instagram](https://instagram.com/yourprofile) |  Contact: support@yourcompany.com  
        © 2024 Your Company. All rights reserved.
        """, unsafe_allow_html=True
    )

# Run the app
if __name__ == "__main__":
    Home()
