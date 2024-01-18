import re
import string

import numpy as np

# %%

texts = [
    "Now here's my email: johndoe@gmail.com",
    "Hello can you see this link: https://www.google.com",
    "Hello can you see this link: www.google.com",
    "Hello can you see this link: google.com",
    "We now have a lot of spaces     here, this   should be fixed",
    "We're having a party 🥳🥳",
    "Deal with these accented characters: Publiée Code de référence",
    "Ah CSV, couldn't deal any easier wih these linux lines\n.",
    "Neither could we deal with these Mac Classic lines \r.",
    "Neither could we deal with these MS DOS lines \r\n.",
    "These math: 4x5=20",
    "These usernames, @joe and @doe are the same person",
    "Ahh programmers, always mixing numbers in words Text2Vec, raduis22. Let's drink some 7up.",
    "Whats the epoch: probably 01/01/1970. ",
    "I'm in the 8.30 AM - 5:44PM shift.",
    "With this job, you can earn up to £37,000 per Annum",
    "Your dates should be in the format: dd/mm/yyyy or d/m/y.",
    'What fucking language is this: "Ben je leergierig, pro-actief en is '
    'kwaliteit jouw ding, dan zijn wij op zoek naar jou!"',
    "We might have some <bold>bold</bold> html, probably a <br /> too",
    "What is this:     . Yes there is something before that full stop",
    "Is it possible to Earn $190.00+ Per Day?",
    "Tagged as #tag ##foly, close together #tagged#follied.",
    "Phones 1-800-903-4103",
    "Html &nbsp non-breaking space here",
    "This makes no sense: Electrical Engineer2019-08-30T19:45:11.967.",
    "Instead of <br/> we could use the non-breaking space &nbsp&nbsp or &nbsp",
]


# %%
#  lowercase = tf.strings.lower(input_data)
#     stripped_html = tf.strings.regex_replace(lowercase, "<br />", " ")
#     return tf.strings.regex_replace(
#         stripped_html, f"[{re.escape(string.punctuation)}]", ""
#     )


def sub_regex(input_data_: list[str], pattern: str, rewrite: str = " "):
    pattern = re.compile(pattern)
    return list(map(lambda string_: pattern.sub(rewrite, string_), input_data_))
    pass


# %%


def remove_html_tags(input_data):
    """
    :param input_data: string array, the source strings to process
    :return: new array of processed strings
    """
    return sub_regex(input_data, r"</?\s*\w+\s*/?>")
    pass


def remove_html_char_ent(input_data):
    """
    :param input_data: string array, the source strings to process
    :return: new array of processed strings
    """
    return sub_regex(input_data, r"&\w+")
    pass


def remove_newlines(input_data):
    """
    :param input_data: string array, the source strings to process
    :return: new array of processed strings
    """
    return sub_regex(input_data, r"[\r\n]")


def remove_url_emails(input_data):
    """
    :param input_data: string array, the source strings to process
    :return: new array of processed strings
    """
    # Sourced from https://stackoverflow.com/a/48689681
    reg = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"
    return sub_regex(input_data, reg)
    pass


def remove_mentions(input_data):
    """
    :param input_data: string array, the source strings to process
    :return: new array of processed strings
    """
    reg = r"@\w+"
    return sub_regex(input_data, reg)
    pass


def remove_punctuation(input_data):
    """
    :param input_data: string array, the source strings to process
    :return: new array of processed strings
    """
    # Add more punctuations if possible
    punctuations = string.punctuation
    reg = f"[{re.escape(punctuations)}]"
    return sub_regex(input_data, reg)
    pass


import unicodedata


def _remove_accent(sent: str) -> str:
    sent = unicodedata.normalize("NFD", sent).encode("ascii", "ignore").decode("utf-8")
    return sent


def remove_emojis(input_data):
    """
    :param input_data: string array, the source strings to process
    :return: new array of processed strings
    """
    reg = (
        "(["
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"
        "])"
    )
    return sub_regex(input_data, reg)
    pass


def remove_word_digits(input_data):
    """
    :param input_data: string array, the source strings to process
    :return: new array of processed strings
    """
    return sub_regex(input_data, r"\W*\d\w*")
    pass


def remove_extra_spaces(input_data):
    """
    :param input_data: string array, the source strings to process
    :return: new array of processed strings
    """
    return sub_regex(input_data, r"\s{2,}")
    pass


def lowercase(input_data: list[str]):
    return list(map(str.lower, input_data))
    pass


import contractions


def list_map(func, iterable):
    return list(map(func, iterable))
    pass


def expand_contractions(input_data: list[str]):
    return list_map(contractions.fix, input_data)
    pass


def remove_accents(input_data: list[str]):
    return list_map(_remove_accent, input_data)
    pass


# %%

# %%
# These text preprocessing steps act on tokens/words

from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))


def remove_stopwords(word_: str, stop_list=None) -> str:
    if stop_list is None:
        stop_list = stop_words
        pass
    return "" if word_ in stop_list else word_


from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


def lemma(word_: str) -> str:
    return lemmatizer.lemmatize(word_)
    pass


from nltk.tokenize import word_tokenize


def apply_to_tokens(sent: str, *functors):
    tokens = word_tokenize(sent)

    def call_functors(word_) -> str:
        for func in functors:
            word_ = func(word_)
            pass
        return word_
        pass

    return " ".join(list(map(call_functors, tokens)))
    pass


# tmp_input_data = None
def remove_stopwords_and_lem(input_data):
    return list_map(
        lambda string_: apply_to_tokens(string_, remove_stopwords, lemma), input_data
    )
    pass


# %%
# Ultimate Text Pre-processing
def ultimate_text_preprocessing(input_data_: np.array):
    """
    :param input_data_: string array, the source strings to process
    :return: new array of processed strings
    """

    # Before Tokenization
    # Expand contractions -> Slow CPU
    input_data_ = expand_contractions(input_data_)

    # Remove newlines (replace each newline with a space)
    input_data_ = remove_newlines(input_data_)

    # Remove links (replace each with a space)
    # Remove emails (replace each with a space)
    input_data_ = remove_url_emails(input_data_)

    # Remove html tags
    input_data_ = remove_html_tags(input_data_)

    # Remove html character entities
    input_data_ = remove_html_char_ent(input_data_)

    # Remove @ mentions
    input_data_ = remove_mentions(input_data_)

    # Remove Emojis
    input_data_ = remove_emojis(input_data_)

    # Remove punctuations (replace each with a space)
    input_data_ = remove_punctuation(input_data_)

    # Remove digits and words containing digits
    input_data_ = remove_word_digits(input_data_)

    # Remove extra spaces
    input_data_ = remove_extra_spaces(input_data_)

    # lowercase
    input_data_ = lowercase(input_data_)

    # Deal with accented characters
    # Unicode to ascii -> Slow CPU
    input_data_ = remove_accents(input_data_)

    # After tokenization ---->
    # Remove Stopwords -> Slow CPU
    # Lemmatization -> Slow CPU
    input_data_ = remove_stopwords_and_lem(input_data_)

    # Remove extra spaces
    input_data_ = remove_extra_spaces(input_data_)

    return np.array(input_data_)
    pass


# %%
# ultimate_text_preprocessing(texts)
