documents = [
    {"name": "HR Policy", "category": "HR", "tags": ["leave", "policy", "hr"]},
    {"name": "Leave Rules", "category": "HR", "tags": ["leave", "rules"]},
    {"name": "Python Guide", "category": "Tech", "tags": ["python", "guide"]},
    {"name": "API Standards", "category": "Tech", "tags": ["python", "api", "rules"]}
]
unique_tag =set()
hr_tag=set()
tech_tag=set()
count={}



for doc in documents:
    unique_tag.update(doc["tags"])
    if doc["category"]=="HR":
        hr_tag.update(doc["tags"])
    else:
        tech_tag.update(doc["tags"])

    for tag in doc["tags"]:
        if tag in count:
            count[tag]+=1
        else:
            count[tag]=1

print("Unique tags:",len(unique_tag),unique_tag)

Uniou_tags=hr_tag & tech_tag 
print("Print common tag: " ,Uniou_tags)

print("number of tags:",count)
print("Maximun number tag appear: ",max(count.values()),tag)

print("Mapping of tags-----")
tag_mapping= {}
for doc in documents:
    for tag in doc["tags"]:
        if tag not in tag_mapping:
            tag_mapping[tag]=[]
        tag_mapping[tag].append(doc["name"])

print(tag_mapping)