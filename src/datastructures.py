
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name

       
        self._members = []

    
    def _generateId(self):
        return randint(0, 99999999)

    def add_member(self, member):
      
       
        member['id'] = self._generateId()
        self._members.append(member)
        return member
       
    def delete_member(self, id):

        for member in self._members:
            if member['id'] == id:
                self._members.remove(member)
                return True
        return False

    def get_member(self, id):
    
        for member in self._members:
            if member['id'] == id:
                return member
        
      

 
    def get_all_members(self):
        return self._members





