import instagrapi
import datetime 





class Source():
    valid_types = ["Image", "Video"]
    def __init__(self, url, type='Image'):
        self.__url = url        
        self.__type = type 

    @property
    def url(self): return self.__url
    @property
    def type(self): return self.__type




class Post():
    valid_types = ["Instagram", "Twitter", "Facebook"]
    def __init__(self,
        timestamp,
        type="Instagram",
        sources=None, # list of Source Objects
        caption=None,
        location=None    
    ):
        self.__timestamp =timestamp
        self.__type = type
        self.__sources = sources
        self.__caption = caption
        self.__location = location

    @property
    def type(self): return self.__type
    @property
    def timestamp(self): return self.__timestamp
    @property
    def sources(self): return self.__sources
    @property
    def caption(self): return self.__caption
    @property
    def location(self): return self.__location





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
                posts_pre_processed = [] # pre-processed into list of "Post" objects

                for post in posts:
                    dict_ = post.__dict__




                    timestamp = dict_["taken_at"]
                    caption = dict_["caption_text"]

                    loc = dict_["location"]
                    if loc is None: location = None
                    else: location = [loc.__dict__["name"], loc.__dict__["city"]]


                    # How to get media sources? (or simply "sources")
                    posts_pre_processed.append(
                        Post(
                            timestamp,
                            type="Instagram",
                            caption=caption,
                            location=location
                        )
                    )

                return posts_pre_processed

        else: # private mode
            raise NotImplementedError('"Private"-mode not yet implemented!')



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
        for key, value in post.__dict__.items():
            print(key, value)




    ''' Testing public mode '''


