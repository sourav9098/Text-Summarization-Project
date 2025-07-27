import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = """Kohli's junior cricket career kicked off in October 2002 at the Luhnu Cricket Ground against Himachal Pradesh. His first half-century in domestic cricket happened at Feroze Shah Kotla, where he scored 70 runs against Haryana.[1] ..."""  # truncated for brevity

def summarizer(rawdocs):
    stop_words = list(STOP_WORDS)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(rawdocs)

    # Build word frequency dictionary
    word_freq = {}
    for word in doc:
        word_lower = word.text.lower()
        if word_lower not in stop_words and word_lower not in punctuation:
            word_freq[word.text] = word_freq.get(word.text, 0) + 1

    max_freq = max(word_freq.values())
    for word in word_freq:
        word_freq[word] /= max_freq

    # Score each sentence
    sent_scores = {}
    for sent in doc.sents:
        for word in sent:
            word_text = word.text
            if word_text in word_freq:
                sent_scores[sent] = sent_scores.get(sent, 0) + word_freq[word_text]

    # Select top sentences
    sent_token = list(doc.sents)
    select_len = max(1, int(len(sent_token) * 0.3))
    summary_sentences = nlargest(select_len, sent_scores, key=sent_scores.get)

    # Combine sentences into summary
    final_summary = [sent.text for sent in summary_sentences]
    summary = ' '.join(final_summary)

    return summary, doc, len(rawdocs.split()), len(summary.split())

# Example usage
summary, doc_obj, orig_len, summ_len = summarizer(text)
print("Summary:\n", summary)
print(f"\nOriginal Length: {orig_len} | Summary Length: {summ_len}")