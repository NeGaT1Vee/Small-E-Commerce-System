
from exceptions import ValidationError


class Category():
    def __init__(self , category_id : str , name : str):

        if not isinstance(category_id , str) or not category_id.strip():
            raise ValidationError("there must be category id which cant be empty text ")

        if not isinstance(name , str):
            raise ValidationError("name must be string")
            
        self._category_id = category_id
        self.name = name 

    property
    def category_id(self):
        return self._category_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, NewName : str):
        if not isinstance(NewName, str) or not NewName.strip():
            raise ValidationError("new category name cant be empty and must be string")
        self._name = NewName.strip()


    ## tells us how many products in the list of prdocuts we given the fucntion have the same category id
    def count_products(self , products :list):
        counter = 0
        for product in products:
            if product.category.category_id == self.__category_id:
                counter +=1
        return counter