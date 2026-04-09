import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKeyv0409.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

doc = {
  "name": "徐梓恩",
  "mail": "1092075@pu.edu.tw",
  "lab": 876
}

doc_ref = db.collection("靜宜資管").document("xuzien")
doc_ref.set(doc)
