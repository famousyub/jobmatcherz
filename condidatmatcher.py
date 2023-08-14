import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample candidates with their skills
candidates = {
    'Candidate 1': 'python machine learning data analysis',
    'Candidate 2': 'java software development database',
    'Candidate 3': 'python data science deep learning',
}

# Sample job offers with required skills
job_offers = {
    'Job Offer 1': 'python machine learning nltk',
    'Job Offer 2': 'java software development',
    'Job Offer 3': 'python data science',
}

def preprocess_text(text):
    # Tokenize and remove punctuation and lowercase
    words = nltk.word_tokenize(text)
    words = [word.lower() for word in words if word.isalpha()]
    return ' '.join(words)



def   matchers(user_skills,offres):
    
    preprocessed_candidates = {name: preprocess_text(skills) for name, skills in  user_skills.items()}
    preprocessed_job_offers = {name: preprocess_text(skills) for name, skills in  offres.items()}

    # Create a corpus of skills (candidates' skills and job offers' skills)
    corpus = list(preprocessed_candidates.values()) + list(preprocessed_job_offers.values())

    # Create a TF-IDF vectorizer to convert the skills into numerical vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)


    # Match each candidate to the best-fitting job offer based on cosine similarity
    for candidate_name, candidate_vector in preprocessed_candidates.items():
        candidate_tfidf = vectorizer.transform([candidate_vector])
        similarities = cosine_similarity(candidate_tfidf, tfidf_matrix)
        best_match_index = similarities.argmax()
        best_match_job_offer = list(preprocessed_job_offers.keys())[best_match_index]
        print(f"Candidate '{candidate_name}' best matches with Job Offer '{best_match_job_offer}'")


        try : 

            return  f"{candidate_name}' best matches with Job Offer '{best_match_job_offer}"


        except  Exception as ex :
            return f'{str(ex)}'







