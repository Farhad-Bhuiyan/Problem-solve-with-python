class MobilePhone:
    
    def __init__(self,model,battery=100):
        self.model=model
        self._battery=battery
        
    def use(self,amount):
        self._battery=max(0,self._battery-amount)
        
    def charge(self,amount):
        self._battery=min(100,self._battery+amount)
        
    def get_charge(self):
        return self._battery
    
    
phone = MobilePhone("Galaxy S24")
print(f"Model (public): {phone.model}")

x = phone.get_charge()   # 100
print(x)
phone.use(30)             # 70
phone.use(50)             # 20
phone.charge(30)          # 50
phone.charge(80)          # 100 (capped)
y = phone.get_charge()   # 100
print(y)
