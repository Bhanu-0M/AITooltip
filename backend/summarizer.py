import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt_tab')

# def summarize_article(url):
    # import google.generativeai as genai
    # import requests
    
    # GEMINI_API_KEY = "AIzaSyALdm36RUxfdJ9c7zY-nvzL4d2gay_RR34"
    # genai.configure(api_key=GEMINI_API_KEY)

    # try:
    #     response = requests.get(url)
    #     response.raise_for_status()
    #     soup = BeautifulSoup(response.content, 'html.parser')
        
    #     article_text = ""
    #     article_elements = soup.find_all(['p', 'h1', 'h2', 'h3'])
    #     if article_elements:
    #         for element in article_elements:
    #             article_text += element.text + " "
    #     else:
    #         article_text = soup.body.get_text()

    #     print("Article Text Retrieved...")

    #     if not article_text.strip():
    #         return "Error: Could not extract article text. The website structure may be incompatible."

    #     print("Generating AI Summary...")

    #     model = None
    #     try:
    #         model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    #     except Exception as e:
    #         print(f'Error: Could not initialize the model. Please check your API key and model name. Error: {e}')

    #     if model is None:
    #         return "Error: Failed to initialize generative model"

    #     prompt = f"""Please provide a concise summary of the following article:
        
    #     {article_text}
        
    #     Provide a summary in 3-4 sentences."""

    #     print("Prompt:", prompt)

    #     response = model.generate_content(prompt)
    #     summary = response.text
    #     print(summary)

    #     return summary

    # except requests.exceptions.RequestException as e:
    #     return f"Error: Could not retrieve article from URL: {e}"
    # except Exception as e:
    #     return f"An error occurred: {e}"

#Using NLP (NLTK) previously done

def summarize_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        article_text = ""
        article_elements = soup.find_all(['p', 'h1', 'h2', 'h3'])
        if article_elements:
            for element in article_elements:
                article_text += element.text + " "
        else:
            article_text = soup.body.get_text()
        if not article_text.strip():
            return "Error: Could not extract article text.  The website structure may be incompatible."

        try:
            nltk.data.find('punkt')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.data.find('stopwords')
        except LookupError:
            nltk.download('stopwords')

        sentences = sent_tokenize(article_text)
        words = word_tokenize(article_text)
        stop_words = set(stopwords.words('english'))

        word_frequencies = {}
        for word in words:
            word = word.lower()
            if word.isalnum() and word not in stop_words:
                if word in word_frequencies:
                    word_frequencies[word] += 1
                else:
                    word_frequencies[word] = 1

        max_frequency = max(word_frequencies.values())
        sentence_scores = {}
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in word_frequencies:
                    if sentence in sentence_scores:
                        sentence_scores[sentence] += word_frequencies[word] / max_frequency
                    else:
                        sentence_scores[sentence] = word_frequencies[word] / max_frequency

        num_sentences = min(5, len(sentences))
        top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
        summary = " ".join(top_sentences)

        return summary

    except requests.exceptions.RequestException as e:
        return f"Error: Could not retrieve article from URL: {e}"
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    article_url = input("Enter the URL of the article to summarize: ")
    summary = summarize_article(article_url)
    print("\nSummary:")
    print(summary)