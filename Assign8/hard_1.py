catalog = [ 
    {"id": 1, "title": "Stranger Signals",     "tags": ["scifi", "thriller"]}, 
    {"id": 2, "title": "Bake Masters",         "tags": ["cooking", "reality"]}, 
    {"id": 3, "title": "Deep Space Diaries",   "tags": ["scifi", "drama"]}, 
    {"id": 4, "title": "Courtroom Chronicles", "tags": ["drama", "legal"]}, 
    {"id": 5, "title": "Galaxy Frontier",      "tags": ["scifi", "action"]}, 
    {"id": 6, "title": "Street Food Stories",  "tags": ["cooking", "travel"]}, 
    {"id": 7, "title": "The Last Algorithm",   "tags": ["thriller", "tech"]}, 
    {"id": 8, "title": "Robot Uprising",       "tags": ["scifi", "action", "thriller"]}, 
] 

watched_ids = [1, 3, 5]

profile={}
def build_profile(catalog,watched_ids):
    for data  in catalog:
        if data["id"] in watched_ids:
            for tag in data["tags"]:
               if tag in profile:
                   profile[tag]+=1
               else:
                   profile[tag]=1
            
    return profile
           
def score_title(title,profile):
    score=0
    for tag in title:
        pass


def recommend(catalog,watched_ids,top_n=3):
    pass

print(build_profile(catalog,watched_ids))
