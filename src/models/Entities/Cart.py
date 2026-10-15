from src.models.Entities import CartItem,Product 
class Cart:
    def __init__(self,items:list[CartItem]):
        self.items=items
    #items validation
    @property
    def items(self):
        return self.__items
    @items.setter
    def items(self,new_items):
        if not isinstance(new_items,list):
            raise TypeError("new_items must be a list")
        for item in new_items:
            if not isinstance(item,CartItem):
                raise TypeError("item must be an object of CartItem")
        self.__items=new_items
            
    #methods:-
    #1-add_item
    def add_item(self,product:Product,quantity):
        item=CartItem(product,quantity)
        self.__items.append(item)
    #2-remove item
    def remove_item(self,item):
        try:
            self.__items.remove(item)
        except:
            raise ValueError("item is not in the list")
        
    #3-total
    def total(self):
        total=0
        for item in self.__items:
            total+=item.quantity*item.product.price
        return total
    #4-is empty
    def is_empty(self):
        return len(self.items)==0
    #5-clear
    def clear(self):
        self.items.clear()