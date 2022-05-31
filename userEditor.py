from cryptography.fernet import Fernet
import os
key= b'oWp9rSuqY8r1CPAkxWjlNkIy_C3PD4JeMFvxNmSdZiQ='
spttext = "D6SFDSDJEFJDNUFJ47H238743HFBSDJAKHNDNSMAJDNAHDJUEHAJDMAHNNMCNYENDJ432HG"
crypter = Fernet(key)

def encrypt(text):

    return crypter.encrypt(str(text).encode()).decode()

def decrypt(text):
    #crypter.decrypt(str(text).encode())
    return crypter.decrypt(text.encode()).decode()

class userEditor:
    def getUserData(username):
        try:
            theline = open("users/{}.txt".format(username),"r").readlines()[0]
            
            
            return {
                "username":decrypt(theline).split(spttext)[0],
                "password":decrypt(theline).split(spttext)[1],
                "fullName":decrypt(theline).split(spttext)[2],
                "avatar":decrypt(theline).split(spttext)[3]
            }
        except:
            return 404

    def getUserList():
        users = []
        userFiles = os.listdir("users")
        for u in userFiles:
            users.insert(0,u.replace(".txt",""))

        return users
