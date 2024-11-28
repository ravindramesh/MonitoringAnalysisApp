import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Function to get top n-grams
def get_top_ngrams(corpus, n=1, top_n=50):
    vectorizer = CountVectorizer(ngram_range=(n, n))
    X = vectorizer.fit_transform(corpus)
    ngram_counts = Counter(dict(zip(vectorizer.get_feature_names_out(), X.toarray().sum(axis=0))))
    return ngram_counts.most_common(top_n)

# Callback functions for deletion
def delete_bigram(index):
    if index < len(st.session_state.bigrams_display):
        st.session_state.bigrams_display.pop(index)
        if st.session_state.bigrams_remaining:
            st.session_state.bigrams_display.append(st.session_state.bigrams_remaining.pop(0))

def delete_trigram(index):
    if index < len(st.session_state.trigrams_display):
        st.session_state.trigrams_display.pop(index)
        if st.session_state.trigrams_remaining:
            st.session_state.trigrams_display.append(st.session_state.trigrams_remaining.pop(0))

# Generate a word cloud from the combined n-grams
def generate_combined_wordcloud(bigrams, trigrams):
    # Combine the bi-grams and tri-grams
    combined_ngrams = bigrams + trigrams
    word_freq = dict(combined_ngrams)
    
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_freq)
    
    # Display the word cloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)

# Streamlit app
def main():
    st.title("Word Cloud Generator")
    st.write("Upload a CSV file and analyze the top two- and three-word phrases from the 'Headline' column.")

    # File uploader
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        # Validate input
        if 'Headline' not in df.columns:
            st.error("The file does not contain a column named 'Headline'. Please upload a valid file.")
            return

        st.write("Preview of the uploaded file:")
        st.write(df.head())

        # Extract headlines
        headlines = df['Headline'].dropna().astype(str).tolist()

        # Generate n-grams
        bigrams = get_top_ngrams(headlines, n=2, top_n=50)
        trigrams = get_top_ngrams(headlines, n=3, top_n=50)

        # Initialize session state
        if "bigrams_display" not in st.session_state:
            st.session_state.bigrams_display = bigrams[:10]
            st.session_state.bigrams_remaining = bigrams[10:]

        if "trigrams_display" not in st.session_state:
            st.session_state.trigrams_display = trigrams[:10]
            st.session_state.trigrams_remaining = trigrams[10:]

        # Display bi-grams and tri-grams in two columns
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Top Two-word Phrases")
            for i, (bigram, freq) in enumerate(st.session_state.bigrams_display):
                col_a, col_b = st.columns([4, 1])
                col_a.write(f"{bigram} ({freq})")
                col_b.button("Del", key=f"delete_bigram_{i}", on_click=delete_bigram, args=(i,))
            if not st.session_state.bigrams_display:
                st.write("No more bi-grams to display.")

        with col2:
            st.subheader("Top Three-word Phrases")
            for i, (trigram, freq) in enumerate(st.session_state.trigrams_display):
                col_a, col_b = st.columns([4, 1])
                col_a.write(f"{trigram} ({freq})")
                col_b.button("Del", key=f"delete_trigram_{i}", on_click=delete_trigram, args=(i,))
            if not st.session_state.trigrams_display:
                st.write("No more tri-grams to display.")

        # Generate and display combined word cloud for bi-grams and tri-grams
        st.subheader("Combined Word Cloud")
        generate_combined_wordcloud(st.session_state.bigrams_display, st.session_state.trigrams_display)

    
    # Link to go back to the Dashboard
    #st.write("[Back to Dashboard](?page=monitoringanalysis_streamlit)")
    #st.markdown("[Back to Dashboard](?page=monitoringanalysis_streamlit){: target='_self'}:")
    st.markdown("<a href='?page=monitoringanalysis_streamlit' target='_self'>Back to Dashboard</a>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
