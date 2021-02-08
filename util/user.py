from flask_sqlalchemy import SQLAlchemy
from operator import itemgetter
import numpy as np

class CustomException(Exception):
    def __init__(self, exception:str='Custom Error'):
        super().__init__(exception)

class UserConfig():
    def __init__(self, super_class, current_user):
        self.current_user = current_user
        self.super_class = super_class.query.all()

    
    def get_posts(self, user_id:int=0, autocomplete_user:bool=True) -> list:
        try:
            assert isinstance(user_id, int)
            assert isinstance(autocomplete_user, bool)
        
        except AssertionError:
            CustomException('TypeError')

        if autocomplete_user:
            user_id = user_id if user_id else self.current_user.id
        
        else:
            user_id = None

        posts_array = np.array(list())
        
        for post in self.super_class:
            if not user_id:
                posts_array.append((post.id, post.name, post.post_date, post.title, post.content)) 


    def recent_posts(self, user_id:int=0, n_files:int=1) -> list:

        try: 
            assert isinstance(n_files, int)
            assert isinstance(user_id, int)

        except AssertionError:
            raise CustomException('TypeError')
        

        if user_id:
            post_list = self.get_posts(user_id=user_id, autocomplete_user=False)
        else:
            post_list = self.get_posts(autocomplete_user=False)

        output_list = sorted(files_list, key=itemgetter(3))
        output_list.reverse()
        return output_list[:n_files]