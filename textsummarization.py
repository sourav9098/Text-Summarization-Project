import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
text="""Kohli's junior cricket career kicked off in October 2002 at the Luhnu Cricket Ground against Himachal Pradesh. His first half-century in domestic cricket happened at Feroze Shah Kotla, where he scored 70 runs against Haryana.[1] By the end of the season, he had amassed a total of 172 runs, emerging as the highest run-scorer for his side with an average of 34.40.[20] During the 2003 season, Kohli was appointed the captain of the U-15 team. He scored 54 runs in Delhi's victory over Himachal Pradesh. In the next fixture against Jammu and Kashmir, Kohli scored his maiden century with a score of 119. By the end of the season, he had a total of 390 runs at an average of 78, which included two centuries.[21][1] Towards the end of 2004, Kohli earned selection for the 2004 Vijay Merchant Trophy with the Delhi U-17 team. In the four matches that he played, Kohli had a total of 470 runs, with his highest score being 251* runs.
The team's coach, Ajit Chaudhary, lauded his performance and was particularly impressed with his temperament on the field.[1][22] He commenced the 2005 season with a score of 227 against Punjab. Following their victory over Uttar Pradesh in the quarter-finals, Delhi was scheduled to play against Baroda in the semi-finals. The team had high expectations from Kohli, who had promised his coach to finish the job. True to his word, Kohli went on to score 228 runs, leading Delhi to victory. The team later secured the tournament with a five-wicket win over Mumbai, where he contributed with a half-century in the first innings.[1] He ended as the highest run-scorer with a total of 757 runs from 7 matches, averaging 84."""                                                                                                                       
                                                    
        
        
def summarizer(rawdocs):
    stop_word=list(STOP_WORDS)
    nlp = spacy.load("en_core_web_sm")
    doc=nlp(rawdocs)
    tokens=[token.text for token in doc]
    word_freq={}
    for word in doc:
        if word.text.lower() not in stop_word and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text]=1
            else:
                word_freq[word.text]+=1
    max_freq=max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word]=word_freq[word]/max_freq
    sent_token=[sent for sent in doc.sents]
    sent_scores={}
    for sent in sent_token:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent]=word_freq[word.text]
                else:
                    sent_scores[sent]+=word_freq[word.text]


    select_len=int(len(sent_token)*0.3)
    summary=nlargest(select_len,sent_scores,key=sent_scores.get)
    final_summary=[word.text for word in summary]
    summary=' '.join(final_summary)
    return summary,doc,len(rawdocs.split(' ')),len(summary.split(' '))
   