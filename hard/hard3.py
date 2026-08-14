import re
library = {
    "documents": [],
    "categories": set(),
}


def addDocu():
    NextId = len(library["documents"]) + 1
    name = input("enter your Document name : ").strip()
    category = input("Enter the category: ").strip()
    tags = input("Enter the tags: ")

    tag = set()
    for t in tags.split(","):
        tag.add(t.strip().lower())

    print(tag)

    documents = {
        "id": NextId,
        "name": name,
        "category": category,
        "tags": tag
    }

    library["documents"].append(documents)
    library["categories"].add(category)

    print("Document added")


def listDoc():

    if not library["documents"]:
        print("Library is empty.. Please first add data")
        return

    for doc in library["documents"]:
        print(f"[{doc['id']}] {doc['name']} ({doc['category']}) tags: {','.join(doc['tags'])}")


def SearchByCategory():
    if not library["categories"]:
        print("No categories to show")
        return

    category = input("enter the category to search: ")

    for doc in library["documents"]:
        if doc["category"].lower() == category.lower():
            print(f"[{doc['id']}] {doc['name']} ({doc['category']}) tags: {','.join(doc['tags'])}")


def searchByTag():
    if not library["documents"]:
        print("Enter data first")
        return
               

    tag_input = input("Enter the tag: ").strip().lower()

    for doc in library["documents"]:
        
        for tag in doc["tags"]:

            if re.search(tag_input,tag,re.IGNORECASE):
                print(f"[{doc['id']}] {doc['name']} ({doc['category']}) tags: {','.join(doc['tags'])}")


def summary():

    print("=====Library Summary====")

    if not library["documents"]:
        print("No summary to view")
        return

    document = 0
    category = set()
    unique_tag = set()
    maxDoc = 0

    for doc in library["documents"]:
        document += 1
        category.add(doc["category"])
        unique_tag.update(doc["tags"])

    print(f"Documents: {document}, Category: {category}, uniqueTag={unique_tag}")


while True:

    print("""
=== AI Knowledge Assistant - Library ===
1. Add Document
2. List Documents
3. Search by Category
4. Search by Tag
5. Library Summary
6. Exit
""")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        addDocu()
    elif choice == 2:
        listDoc()
    elif choice == 3:
        SearchByCategory()
    elif choice == 4:
        searchByTag()
    elif choice == 5:
        summary()
    elif choice == 6:
        print("Exit !!")
        break
    else:
        print("invalid choice")