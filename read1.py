import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKeyv0409.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

doc_ref = db.document("靜宜資管/xuzien")
doc = doc_ref.get()
result = doc.to_dict()
print(f"姓名:{result["name"]},研究室在{result["lab"]},電子郵件為{result["mail"]}")

#靜宜資管/xuzien中所需要的相關資料顯示出來