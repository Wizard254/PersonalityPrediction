from nltk.tokenize import word_tokenize
import string
from nltk.stem import WordNetLemmatizer
import nltk

import os
import joblib
from old.streamlitjobcategorypred import pred_job_category
import fitz
import uuid

# import aspose.words as aw

# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')

punctuation = string.punctuation + "‘" + "~" + "“" + "”" + "„" + "‟" + "’" + "‚" + "‛"
wordnet_lemmatizer = WordNetLemmatizer()
stopwords = nltk.corpus.stopwords.words("english")

clf = joblib.load("streamlit/knn_classifier.model.pkl")
vectorizer = joblib.load("streamlit/vectorizer.pkl")


def get_mbti(pdf_text):
    # pdf_text = "She likes to stay at home, not to interact with anyone"

    def text_preprocessing(sentences: str):
        # Tokenization
        words = word_tokenize(sentences)

        # Remove Punctuations
        out_words = []
        for word in words:
            broke = False
            for c in word:
                if c in punctuation:
                    broke = True
                    break
                    pass
                else:
                    pass
                pass

            if not broke:
                out_words.append(word)
                pass
            pass
        words = out_words
        del out_words
        # words = [word for word in words if punctuation not in word]

        # Lemmatization
        # defining the object for Lemmatization
        words = [wordnet_lemmatizer.lemmatize(word) for word in words]

        # Lower casing the text
        words = [word.lower() for word in words]

        # Stop Word Removal
        words = [word for word in words if word not in stopwords]

        return " ".join(words)
        pass

    processed_text = text_preprocessing(pdf_text)
    x_sample = vectorizer.transform([processed_text])

    return clf.predict(x_sample)
    pass


mbti_summaries = {
    "ISTJ": "ISTJs are responsible, organized, and dependable. They value stability, tradition, and follow rules "
            "diligently.",
    "ISFJ": "ISFJs are warm, caring, and detail-oriented individuals. They are loyal, practical, and committed to "
            "helping others.",
    "INFJ": "INFJs are insightful, compassionate, and idealistic. "
            "They have a deep understanding of others and are driven by their values.",
    "INTJ": "INTJs are logical, strategic, and independent thinkers. "
            "They are highly analytical and excel in long-term planning.",
    "ISTP": "ISTPs are adventurous, analytical, and practical problem solvers. "
            "They are independent and enjoy hands-on activities.",
    "ISFP": "ISFPs are gentle, sensitive, and artistic individuals. "
            "They appreciate beauty, nature, and enjoy "
            "expressing themselves creatively.",
    "INFP": "INFPs are empathetic, creative, and idealistic. "
            "They strive for harmony, deeply value authenticity, and seek meaning in life.",
    "INTP": "INTPs are curious, logical, and original thinkers. "
            "They enjoy exploring abstract concepts and solving complex problems.",
    "ESTP": "ESTPs are energetic, outgoing, and action-oriented individuals. "
            "They are adaptable, quick thinkers, and enjoy new experiences.",
    "ESFP": "ESFPs are enthusiastic, spontaneous, and fun-loving individuals. "
            "They thrive in social settings and enjoy entertaining others.",
    "ENFP": "ENFPs are enthusiastic, imaginative, and empathetic. "
            "They are passionate about personal growth, possibilities, and connecting with others.",
    "ENTP": "ENTPs are innovative, quick-witted, and resourceful thinkers. "
            "They enjoy intellectual debates, problem-solving, and exploring new ideas.",
    "ESTJ": "ESTJs are practical, efficient, and organized individuals. "
            "They are natural leaders, value structure, and strive for success.",
    "ESFJ": "ESFJs are warm, social, and dedicated individuals. "
            "They are responsible, supportive, and enjoy creating a harmonious environment.",
    "ENFJ": "ENFJs are charismatic, empathetic, and inspiring individuals. "
            "They are natural leaders, motivators, and care deeply about others.",
    "ENTJ": "ENTJs are strategic, logical, and assertive leaders. "
            "They have strong leadership skills, focus on "
            "efficiency, and excel in planning and organizing.",
}


def predict_mbti_category(file) -> (str, str):
    hex_ = uuid.uuid4().hex
    txt_resume_file = hex_ + ".txt"

    # checking if the directory demo_folder
    # exist or not.
    out_dir = "out/"
    if not os.path.exists(out_dir):
        # if the demo_folder directory is not present
        # then create it.
        os.makedirs(out_dir)
        pass

    txt_resume_file = f"{out_dir}{txt_resume_file}"

    doc = fitz.Document(file)  # open a document
    out = open(txt_resume_file, "wb")  # create a text output
    for page in doc:  # iterate the document pages
        text = page.get_text().encode("utf8")  # get plain text (is in UTF-8)
        out.write(text)  # write text of page
        # out.write(bytes((12,)))  # write page delimiter (form feed 0x0C)
        pass
    out.close()

    # mbti_type = None
    with open(txt_resume_file, encoding='utf-8') as fp:
        contents = " ".join(fp.readlines())
        mbti_type = get_mbti(contents)
        pass

    mbti_type = mbti_type[0]
    job_category = pred_job_category(contents)

    return mbti_type, job_category
    pass
