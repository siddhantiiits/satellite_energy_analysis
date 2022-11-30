from firebase_admin import credentials, initialize_app, storage
# Init firebase with your credentials
cred = credentials.Certificate("serviceac.json")
initialize_app(cred, {'storageBucket': 'brames-3cf3b.appspot.com/'})

# Put your local file path
fileName = "Satellite Images/London/London_Energy+PD+GC.png"
bucket = storage.bucket('brames-3cf3b.appspot.com')
blob = bucket.blob('maps_output/outputimg.jpg')
blob.upload_from_filename(fileName)

# Opt : if you want to make public access from the URL
# blob.make_public()

# print("your file url", blob.public_url)