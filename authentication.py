import pyrebase

config = {
  'apiKey': "AIzaSyDIWINaH8Q7cBshxqzDcHphJKLWvRRELQc",
  'authDomain': "blissful-cell-393422.firebaseapp.com",
  'projectId': "blissful-cell-393422",
  'storageBucket': "blissful-cell-393422.appspot.com",
  'messagingSenderId': "208919849448",
  'appId': "1:208919849448:web:f03dd4ad2812f3b81f5c5d",
  'measurementId': "G-D9FPTHTPYW",
  'databaseURL': " "
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

email = 'test@gmail.com'
password = 'test1234567'


#user = auth.create_user_with_email_and_password(email, password)
#print(user)

user = auth.sign_in_with_email_and_password(email, password)

#info = auth.get_account_info(user['idToken'])
#print(info)

#auth.send_email_verification(user['idToken'])
#auth.send_password_reset_email(email)