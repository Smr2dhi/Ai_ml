import logging
import json
import requests

logging.basicConfig(
	filename='logFile.log',
	level=logging.INFO,
	format='%(asctime)s - %(levelname)s- %(message)s'
	
)
logger=logging.getLogger(__name__)

class Documents:
	def __init__(self,doc_id:int,name,category,tags,source):
		self.doc_id=doc_id
		self.name=name
		self.category=category
		self.tags={tag.strip().lower() for tag in tags}
		self.source=source
	def describe(self):

		print(f'[{self.doc_id}] {self.name}  {self.category}  {self.source}  {self.tags}')

class DocumentNotFound(Exception):
	pass
class DuplicateDocumentError(Exception):
	pass

class DocumentLibrary:
	
	def __init__(self):
		self.documents={}
		self.count=0

	def add_documents(self,name,category,tags,source):


			for doc in self.documents.values():
				if doc.name.lower()==name.lower():
					logger.error("Duplicate document name")
					raise DuplicateDocumentError("Document already exist!!")

			self.count+=1
			doc_id=self.count

			document=Documents(
				doc_id,
				name,category,tags,source
			)
			self.documents[doc_id]=document

			return document

	def get_documents(self,doc_id):
			if doc_id not in self.documents:
				logger.error("No doc found ,invalid id")
				raise DocumentNotFound("No such document exists")
			return self.documents[doc_id]

	def remove_documents(self,doc_id):

		if doc_id not in self.documents:
			logger.error("No sunch doc found")
			raise DocumentNotFound("No doc exists")
		
		document=self.documents.pop(doc_id)
		return document


	def search_by_tags(self,tags):
		result=[]

		tags=tags.strip().lower()

		for doc in self.documents.values():
			if tags in doc.tags:
				result.append(doc)

		return result

	def summary(self):
		unique_tags=set()
		category_count={}
		source_count={}

		print("Total doc: ", len(self.documents))
		for doc in self.documents.values():

			category_count[doc.category]=(
				category_count.get(doc.category,0)+1
			)

			source_count[doc.source]=(
				source_count.get(doc.source,0)+1
			)

			unique_tags.update(doc.tags)

		print("Count per category:", category_count)
		print("Count per source:", source_count)
		print("All unique tags:", unique_tags)	


	def save_to_json(self,path):
		data=[]
		for doc in self.documents.values():
			doc_data={
				"doc_id":doc.doc_id,
				"name":doc.name,
				"category":doc.category,
				"tags":sorted(doc.tags),
				"source":doc.source
			}
			data.append(doc_data)

		with open(path,"w")as file:
			json.dump(data,file,indent=4)
			logger.info("file save to json file")

	def load_from_json(self,path):
		try:
			with open(path,"r")as file:
				data=json.load(file)

			self.documents={}

			for item in data:
				document=Documents(
					item["doc_id"],
					item["name"],
					item["category"],
					set(item["tags"]),
					item["source"]
					
				)

				self.documents[document.doc_id]=document

			if self.documents:
				self.count=max(self.documents.keys())
			else:
				self.count=0

		except FileNotFoundError:
			print("No saved library - starting empty.")
			self.documents={}
			self.count=0

		except json.JSONDecodeError:
			print("Library file is corrupted - starting empty.")
			self.documents={}
			self.count=0

	def import_from_api(self,library):
		url="https://jsonplaceholder.typicode.com/posts?userId=1"
		imported=0
		skipped=0

		try:
			response=requests.get(url,timeout=10)
			response.raise_for_status()

			posts=response.json()

			for post in posts:
				try:
					library.add_documents(
						name=post['title'],
						category="external",
						tags={"api","imported"},
						source="api"
					)
					imported+=1

				except DuplicateDocumentError:
					skipped+=1

			print(f"Imported {imported} documents, skipped {skipped} duplicates.")

		except requests.exceptions.RequestException as e:
			print(f"Import failed: {e}")


def addDocument():
	try:
		name=input("Document name: ").strip()
		category=input("Category: ").strip()
		tags=input("Tags (comma-separated): ")

		tag_set=set()

		for tag in tags.split(","):
			tag=tag.strip().lower()

			if tag:
				tag_set.add(tag)

		document=doc.add_documents(
			name,
			category,
			tag_set,
			"local"
		)

		print("Added: ",end="")
		document.describe()

	except DuplicateDocumentError as e:
		print(e)


def listAll():
	for row in doc.documents.values():
		row.describe()


def searchByTag():
	tag=input("Enter tag: ").strip().lower()

	result=doc.search_by_tags(tag)

	if not result:
		print("No documents found")
		return

	for row in result:
		row.describe()


def removeDocument():
	try:
		doc_id=int(input("Document ID: "))

		document=doc.remove_documents(doc_id)

		print("Removed: ",end="")
		document.describe()

	except ValueError:
		print("Document ID must be a number")

	except DocumentNotFound as e:
		print(e)


def importAPI():
	doc.import_from_api(doc)


def showSummary():
	doc.summary()


def saveLibrary():
	doc.save_to_json("Assign3/jsonFile.json")


doc=DocumentLibrary()

doc.load_from_json("Assign3/jsonFile.json")

while True:

	print("""
=== AI Knowledge Assistant - Library v0.4 ===
1. Add Document
2. List Documents
3. Search by Tag
4. Remove Document
5. Import from API
6. Library Summary
7. Save Library
8. Exit (saves automatically)
""")

	try:
		userInput=int(input("Choice: "))

		if userInput==1:
			addDocument()

		elif userInput==2:
			listAll()

		elif userInput==3:
			searchByTag()

		elif userInput==4:
			removeDocument()

		elif userInput==5:
			importAPI()

		elif userInput==6:
			showSummary()

		elif userInput==7:
			saveLibrary()

		elif userInput==8:
			doc.save_to_json("Assign3/jsonFile.json")
			print("Goodbye!")
			break

		else:
			print("Invalid choice")

	except ValueError:
		print("Please enter a number")

	except Exception as e:
		print("Error:",e)