import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('mod_dev.ignore/discord-bot-status-e749403ddd8b.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

# init doc
doc_ref = db.collection("discord_bot").document("quest")
doc_ref.set(dict(
    data1 = 'hello',
    data2 = 123,
    data3 = [1,2,3]
))

collection = db.collection("discord_bot")
docs = collection.stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')

print('stop')