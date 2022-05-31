from cryptography.fernet import Fernet

key= b'oWp9rSuqY8r1CPAkxWjlNkIy_C3PD4JeMFvxNmSdZiQ='
spttext = "D6SFDSDJEFJDNUFJ47H238743HFBSDJAKHNDNSMAJDNAHDJUEHAJDMAHNNMCNYENDJ432HG"
crypter = Fernet(key)

def encrypt(text):

    return crypter.encrypt(str(text).encode()).decode()

def decrypt(text):
    #crypter.decrypt(str(text).encode())
    return crypter.decrypt(text.encode()).decode()



class auth:
    def sign_up(username,password,fullname,avatar):
        allUsers = open("users.txt","a")
        the_text_to_inject = f"{username}D6SFDSDJEFJDNUFJ47H238743HFBSDJAKHNDNSMAJDNAHDJUEHAJDMAHNNMCNYENDJ432HG{password}"
        allUsers.write(encrypt(the_text_to_inject)+"\n")
        userFile = open("users/{}.txt".format(username),"a")
        userInfo = encrypt(f"{username}D6SFDSDJEFJDNUFJ47H238743HFBSDJAKHNDNSMAJDNAHDJUEHAJDMAHNNMCNYENDJ432HG{password}D6SFDSDJEFJDNUFJ47H238743HFBSDJAKHNDNSMAJDNAHDJUEHAJDMAHNNMCNYENDJ432HG{fullname}D6SFDSDJEFJDNUFJ47H238743HFBSDJAKHNDNSMAJDNAHDJUEHAJDMAHNNMCNYENDJ432HG{avatar}")
        userFile.write(userInfo+"\n")
        return 200
    
    def sign_in(username,password):
        allUsers = open("users.txt","r").readlines()
        for a in allUsers:
            try:
                decrypt(a).split(username)[1]
                theline=a
                break
            except:
                theline = None
                pass
        
        if theline == None:
            return 404
        
        else:
            if decrypt(theline).split(spttext)[1] == password:
                return 200
        
            else:
                return 403
    

