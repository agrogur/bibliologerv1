import pyrebase

config = {
  'apiKey': "[USE YOUR OWN API KEY]",
  'authDomain': "...",
  'projectId': "...",
  'storageBucket': "...",
  'messagingSenderId': "...",
  'appId': "...",
  'measurementId': "...",
  'databaseURL': " "
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

email = ''
password = ''


#user = auth.create_user_with_email_and_password(email, password)
#print(user)

user = auth.sign_in_with_email_and_password(email, password)

#info = auth.get_account_info(user['idToken'])
#print(info)

#auth.send_email_verification(user['idToken'])
#auth.send_password_reset_email(email)
