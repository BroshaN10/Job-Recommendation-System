# jobs/recommendation.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Job

def get_recommendations(user_preferences):
    # Get all jobs
    jobs = Job.objects.all()

    # Create a list of job descriptions
    job_descriptions = [f"{job.title} {job.company} {job.location} {job.description}" for job in jobs]

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')

    # Fit and transform job descriptions
    job_vectors = vectorizer.fit_transform(job_descriptions)

    # Transform user preferences
    user_vector = vectorizer.transform([user_preferences])

    # Calculate cosine similarities
    similarities = cosine_similarity(user_vector, job_vectors).flatten()

    # Get indices of top 10 most similar jobs
    top_indices = similarities.argsort()[-10:][::-1]

    # Return top 10 job recommendations
    return [jobs[i] for i in top_indices]