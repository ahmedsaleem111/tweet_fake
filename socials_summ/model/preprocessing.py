import instagrapi
import datetime 



'''
Specify a dummy root user (to allow access to public accounts)

'''
root_handle = 'socialssumm'
root_password = "SocialsSummRoot!%!%"

class PreProcessor():

    def __init__(self, handle, password=None, year=datetime.datetime.now().year): # get current year by default
        self.__handle = handle
        self.__password = password
        self.__year = year

    @property
    def handle(self): return self.__handle
    @property
    def password(self): return self.__password
    @property
    def year(self): return self.__year
    @property
    def accountType(self):
        if self.password is None: return "public"
        else: return "private"


class InstagramPreProcessor(PreProcessor):

    def __init__(self, handle, password=None, year=datetime.datetime.now().year):
        super().__init__(handle, password=password, year=year)

        self.__root = instagrapi.Client()
        self.__root.login(root_handle, root_password)


        
    def getPosts(self):
        user_id = self.__root.user_id_from_username(self.handle)

        posts = self.__root.user_medias(user_id=user_id, amount=20)

        if self.accountType=="public":
            if len(posts)==0: raise Exception('Specifed account is private. Please provide password!')
            else: 
                posts = [post.__dict__ for post in posts]
                
                return posts
        else: # private account
            return posts # how ?

class TwitterPreProcessor(PreProcessor):

    def __init__(self, handle, password=None, year=datetime.datetime.now().year):
        super().__init__(handle, password=password, year=year)
        


class FacebookPreProcessor(PreProcessor):

    def __init__(self, handle, password=None, year=datetime.datetime.now().year):
        super().__init__(handle, password=password, year=year)






if __name__ == "__main__":

    ''' For Instagram '''


    ''' Testing private mode '''
    ipp = InstagramPreProcessor('ssaleem.ahmedd')

    posts = ipp.getPosts()

    for post in posts: 
        
        print('\n\n\n')
        for key, val in post.items():
            print(key, val)




    ''' Testing public mode '''


