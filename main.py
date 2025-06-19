import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post, make_small_tweaks

tone_options = ["Inspirational", "Storytelling", "Educational", "Opinionated", "Professional", "Casual", "Promotional", "Gratitude", "Philosophical"]
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]

def main():
    st.title("Social Media Post Generator")
    col1, col2, col3, col4, col5 = st.columns(5)
    fs = FewShotPosts()

    with col1:
        selected_name = st.selectbox("Person", options=fs.get_name())

    with col2:
        selected_tag = st.selectbox("Title", options=fs.get_tags_for_name(selected_name))

    with col3:
        selected_tone = st.selectbox("Tone", options=tone_options)

    with col4:
        selected_length = st.selectbox("Length", options=length_options)
    
    with col5:
        selected_language = st.selectbox("Language", options=language_options)
    

    # Session state to hold the generated post
    if 'generated_post' not in st.session_state:
        st.session_state.generated_post = ""
    if 'tweaked_post' not in st.session_state:
        st.session_state.tweaked_post = ""

    if st.button("Generate"):
        st.session_state.generated_post = generate_post(
            selected_name, selected_length, selected_language, selected_tag, selected_tone
        )
        st.session_state.tweaked_post = ""  # Reset any old tweak

    if st.session_state.generated_post:
        st.subheader("Generated Post:")
        st.write(st.session_state.generated_post)

        # Ask for user input to tweak
        user_input = st.text_input("Want to add/change something in the post? Enter here:")

        if user_input:
            if st.button("Make Small Tweaks"):
                st.session_state.tweaked_post = make_small_tweaks(
                    st.session_state.generated_post, user_input, selected_name, selected_length, selected_language, selected_tag
                )

    if st.session_state.tweaked_post:
        st.subheader("Tweaked Post:")
        st.write(st.session_state.tweaked_post)

if __name__ == "__main__":
    main()