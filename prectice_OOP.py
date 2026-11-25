class Person:
    def __init__(self, name, age, height, weight) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
    
    def __gt__(self, other):
        return self.age > other.age

class Cricketer(Person):
    def __init__(self, name, age, height, weight) -> None:
        super().__init__(name, age, height, weight)

sakib = Cricketer('Sakib', 38, 68, 91)
musfiq = Cricketer('Rahim', 36, 68, 88)
kamal = Cricketer('Kamal', 39, 68, 94)
jack = Cricketer('Jack', 38, 68, 91)
kalam = Cricketer('Kalam', 37, 68, 95)


players=[sakib,musfiq,kamal,jack,kalam]

old=players[0]

for player in players[1:]:
    if player > old:
        old = player

print(f"The Oldest Player is {old.name}")
print(f"The Age of the player is {old.age}")
