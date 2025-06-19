from sentence_transformers import SentenceTransformer, util
from few_shot import FewShotPosts
import torch

few_shot = FewShotPosts()

def cal_similarity(generated_post, name, length, language, tag):
    model = SentenceTransformer('all-MiniLM-L6-v2')


    examples = few_shot.get_filtered_posts(name, length, language, tag)

    influencer_posts = []
    for post in examples:
        influencer_posts.append(post['text'])

    #make a list of all influencer text 
    influencer_embeddings = model.encode(influencer_posts, convert_to_tensor=True)
    generated_embedding = model.encode(generated_post, convert_to_tensor=True)

    cos_scores = util.pytorch_cos_sim(generated_embedding, influencer_embeddings)

    # Average similarity
    similarity_score = torch.mean(cos_scores).item()
    print("Similarity score:", round(similarity_score, 2))

    return round(similarity_score, 2)


if __name__ == "__main__":
    cal_similarity("Hello how are you", "Donald Trump", "Short", "English", "Geopolitics")