import pandas as pd
import json


class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        self.df = None
        self.unique_tags = None
        self.unique_names = None
        self.name_to_tags = {}
        self.load_posts(file_path)

    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)
            self.df = pd.json_normalize(posts)
            self.df["length"] = self.df["line_count"].apply(self.categorize_length)

            all_tags = self.df['tags'].apply(lambda x: x).sum()
            self.unique_tags = set(list(all_tags))
            self.unique_names = set(post["name"] for post in posts if "name" in post)

            for post in posts:
                name = post.get("name")
                tags = post.get("tags", [])
                if name:
                    if name not in self.name_to_tags:
                        self.name_to_tags[name] = set()
                    self.name_to_tags[name].update(tags)

            

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"
        
    def get_tags(self):
        return self.unique_tags
    
    def get_name(self):
        return self.unique_names
    
    def get_tags_for_name(self, name):
        if name:
            return sorted(self.name_to_tags.get(name, []))
        else:
            return sorted(self.unique_tags)
    

    def get_filtered_posts(self, name, length, language, tag):
        df_filtered = self.df[
            (self.df['language'] == language) &
            (self.df['length'] == length) &
            (self.df['name'] == name) &
            (self.df['tags'].apply(lambda tags: tag in tags))
        ]
        return df_filtered.to_dict(orient="records")


if __name__ == "__main__":
    fs = FewShotPosts()
    posts = fs.get_filtered_posts("Sundar Pichai", "Short", "English", "Job Search")
