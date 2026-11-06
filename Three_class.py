class Phone:
    
    def __init__(self,model,battery=100):
        self.model=model
        self.battery=battery


class SmartPhone(Phone):
    
    def __init__(self, model,operating_system, battery=100):
        super().__init__(model, battery)
        self.operating_system=operating_system
        
class GamingPhone(SmartPhone):
    
    def __init__(self, model, operating_system,cooling_system, battery=100):
        super().__init__(model, operating_system, battery)
        self.cooling_system=cooling_system
        
    def start_game(self,name):
        print(f"Playing {name} on {self.model}")
        
        
phone = Phone("Nokia 3310")
print(f"Phone: {phone.model}, Battery: {phone.battery}%")

smart = SmartPhone("iPhone 15", "iOS")
print(f"SmartPhone: {smart.model}, OS: {smart.operating_system}, Battery: {smart.battery}%")

gaming = GamingPhone("ROG Phone 7", "Android", "Vapor Chamber")
print(f"GamingPhone: {gaming.model}, OS: {gaming.operating_system}, "
      f"Cooling: {gaming.cooling_system}, Battery: {gaming.battery}%")
gaming.start_game("Genshin Impact")
        

