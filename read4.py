import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

cred = credentials.Certificate("serviceAccountKeyv0409.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

collection_ref = db.collection("靜宜資管")
#docs = collection_ref.where(filter=FieldFilter("mail","==", "tcyang@pu.edu.tw")).get()
docs = collection_ref.order_by("lab",direction=firestore.Query.DESCENDING).limit(5).get()
for doc in docs:
    print("文件內容：{}".format(doc.to_dict()))

#limit(5):排序出lab相關5個資訊
#firestore.Query.DESCENDING (遞減)
#firestore.Query.ASCENDING (遞增)