from llm_helper import llm
from few_shot import FewShotPosts
from similarity import cal_similarity

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "5 to 10 lines"
    if length == "Long":
        return "more than 10 lines"
        


def get_prompt(name, length, language, tag, tone):
    length_str = get_length_str(length)
    prompt = f'''
    You are an expert post writer trained to replicate the writing style of top influencers and profiles.

    Below are example posts written by {name}. Observe the tone, language, structure, and the kind of knowledge, opinions, and type of storytelling they use.. No preamble.

    1. Topic: {tag}
    2. Length: {length_str}
    3. Language: {language}
    4. The tone and vibe of the conversation should be around {tone}
    If Language is Hinglish then it means it is a mix of Hindi and English.
    The script for the generated post should always be English.
    The post should be around recent information and be updated.
    Also include some hashtags at the end.
'''


    examples = few_shot.get_filtered_posts(name, length, language, tag)

    if len(examples) > 0:
        prompt += "5. Strictly use the writing style as per the following example post. Make your post more around these kinds of writing."
        for i, post in enumerate(examples):
            post_text = post['text']
            prompt += f"\n\n Example {i+1}: \n\n {post_text}"

            if i == 9:
                break

    return prompt


def generate_post(name, length, language, tag, tone):

    prompt = get_prompt(name, length, language, tag, tone)
    response = llm.invoke(prompt)

    cos_sim = cal_similarity(response.content, name, length, language, tag)
    while cos_sim < 0.3:
        response = llm.invoke('The similarity score between examples provided and the answer generated are low make more near to the provided writing styles. Your ans = '+response.content+'What I want = '+prompt) 
        cos_sim = cal_similarity(response.content, name, length, language, tag)
    return response.content + str(cos_sim)



def make_small_tweaks(gen_ans, small_tweaks_input, name, length, language, tag):
    prompt = f'''
    In this post make following tweaks and changes: {small_tweaks_input}. No Preamble
    Don't lose the tone, language, structure, and the kind of knowledge, opinions, and type of storytelling they use.

    {gen_ans}
'''
    response = llm.invoke(prompt)

    cos_sim = cal_similarity(response.content, name, length, language, tag)

    while cos_sim < 0.3:
        response = llm.invoke('The similarity score between examples provided and the answer generated are low make more near to the provided writing styles. Your ans = '+response.content+'What I want = '+prompt) 
        cos_sim = cal_similarity(response.content, name, length, language, tag)

    return response.content + str(cos_sim)


if __name__ == "__main__":
    post = generate_post("Sundar Pichai", "Short", "English", "Job Search", "Inspirational")
    print(post)