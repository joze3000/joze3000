
from dataclasses import dataclass, field
from enum import Enum, auto
from random import randint, choice
import logging

#Нужно выполнить задание по логгированию, добавить макс хп, перемещение по локациям, инвентарь и получение предметов, восстановление здоровья, шансы побега.
class Area(Enum):
    plain  =    auto()
    forest =    auto()
    mountain =  auto()
    swamps =    auto()
    ruins  =    auto()

area_name = {
    Area.plain :    "Равнины",
    Area.forest :   "Лес",
    Area.mountain:  "Горы",
    Area.swamps:    "Болота",
    Area.ruins:     "Руины"
}

area_lvl = {
    Area.plain:    range(1,5),
    Area.forest:   range(3,7),
    Area.mountain: range(5,9),
    Area.swamps:   range(7,12),
    Area.ruins:    range(10,15)
}

area_enemy =  {
    Area.plain:     ["Муха","Оса","Жук"],
    Area.forest:    ["Енот","Белка","Бобер(Курва)"],
    Area.mountain:  ["Орел","Горный Козел","Шакал"],
    Area.swamps:    ["Слизняк","Пиявка","Мертвяк"],
    Area.ruins:     ["Боевая кукла","Оживший меч","Скелет-воин"]
}

@dataclass
class Enemy():
    name: str
    lvl: int = 1
    #max_hp = 100
    hp: int = 100
    def __post_init__(self):
        self.give_exp = self.hp
    def damage(self, skill_dmg = 3):
        return int(((self.lvl + 1) * (skill_dmg + randint(-3,3)))/2)
    def __del__(self):
        logging.error(f"DEL ENEMY")
        
@dataclass
class Player():
    name: str
    lvl: int
    max_hp: int = 100
    hp: int = 100
    location: Area = Area.plain
    experience: int = 0
    experience_limit: int = 100
    inventory: list = field(default_factory=list)
    def damage(self, skill_dmg = 5):
        return int(((self.lvl + 10) * (skill_dmg + randint(-3,3)))/2)
    
    def try_lvl_up(self, give_exp):
        self.experience += give_exp
        if self.experience >= self.experience_limit:
            self.lvl += 1
            self.experience_limit += int(self.experience*0.3)
            self.max_hp += int(self.max_hp*0.3)
            self.hp = self.max_hp
            logging.info(f"Поздравляем с получением {self.lvl} уровня")   
        else:
            return 0
    
def main():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('battle.log')
    file_handler.setFormatter(logging.Formatter('%(message)s'))
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    p_info = logging.info
    player = Player("Игрок", 1, 100)
    #found_enemy  = Enemy(choice(area_enemy[player.location]), choice(area_lvl[player.location]), 100)
    #Декоратор для нового врага
    def new_choise(combat):
        travel_choise = input("""Так или иначе ты прошел чуть глубже по локе.
    Вариантов стало куда больше:
1 - Слегка отдохнуть(восстановит немного хп)
2 - Продолжить сражения
3 - Перейти на следующий уровень      
    """)
        # TODO Нужно сделать* Если выбрал 1 - получаем ту же фунцию с другим текстом, но только двумя последующими выборами
        if travel_choise == '1':
            player.hp += player.max_hp*0.3
            p_info(f"Неплохо посидели, подумали о вечном. Вроде как даже отдохнули немного/n Восстановленно {player.max_hp*0.3} здоровья")
            return new_choise(combat)
        elif travel_choise == '2':
            p_info("Фига ты неугомонный фармила. Ну дерзай")
            #combat(player, found_enemy) 
        elif travel_choise == '3':
            player.location = Area((player.location.value)+1)
            p_info(f"""Смело. Ну удачи выжить.
Ты вышел на новую локацию - {area_name[player.location]}
                   """)
            return new_choise(combat)
        else:
            p_info("Давай не безобразничай тут.")
        logger.critical("Функция new_choise закончилась")
    #сырая функция выдачи лута
    def give_loot():
        pass
    #Сырая функция побега
    def try_escape() -> str: 
        p_info("Попытка побега")
        return 'dead' if randint(0, 1) == 0 else 'escape'
    def set_player_name(name):
        if name:
            player.name = name
            p_info(f"Понятно. Очередной {player.name}")
        else:
            player.name = "Игрок"
            p_info("Тогда будешь стандартным Игроком\n")
    def combat(player: Player, found_enemy: Enemy) -> str:
        p_info(f"Ты решил сразиться с {found_enemy.name}, {found_enemy.lvl} уровня!\n Ну давай, заебашь эту тварь")
        while player.hp > 0 and found_enemy.hp > 0:
            player_dmg = player.damage()
            enemy_dmg = found_enemy.damage()
            player.hp -= enemy_dmg
            found_enemy.hp -= player_dmg
            p_info(f"{player.name} Уебал {found_enemy.name} на {player_dmg} единиц урона. Но получил ответку на {enemy_dmg} единиц урона по лицу")
            if player.hp <= 0:
                p_info("Йоу, ты умер.")
                p_info("Записали тебя в позорники")
                return 0
            elif found_enemy.hp <= 0:
                p_info("Туда его. Красава! Завалил гниду.")
                p_info("Ай Маладец!")
                p_info(f"Вы получили {found_enemy.give_exp} опыта")
                player.try_lvl_up(found_enemy.give_exp)
                new_choise(combat)
            else:    
                p_info(f"""У вас осталось {player.hp} здоровья. У вражины {found_enemy.hp}.
Что делаем?
1 - сражайся как мужчина 
2 - в ужасе сьеби в туман""")
                fight_choise = input()
                if fight_choise == '1':
                    p_info("Продолжаем файт")
                #TODO Стоит добавить шанс на побег. *В следующих версиях
                elif fight_choise == '2':
                    p_info("Ты тут вообще то в сражении. Развернувшись ты тут же получил удра в хребет и умер. Лошара")
                    return try_escape()
                else:
                    logging.error("Ты что, тупой? Выбирай нормально")               
    p_info(f"""Привет! Сегодня ты возьмешь на себя роль беттатестера угрюмой хуеты, которая может стать игрой.
Выбора особого у тебя конечно же нет.""")
    name_p =  input("Ну что дружище, как звать то тебя?\n")
    set_player_name(name_p)
    p_info(f"""Ты огляделся. Вокруг {area_name[player.location]}
Внезапно!
На тебя нападает враг!
Так как вариантов у тебя немного, оставляю тебе 2 выбора:
Вариант 1 - ты сражаешься
Вариант 2 - ты умираешь от голода""")
    while True:
        variant = input("Выбирай с умом. И не надо лишнего. Либо 1, либо 2.\n")
        if variant == '1':
            combat(player, found_enemy=Enemy(choice(area_enemy[player.location]), choice(area_lvl[player.location]), 100))
        elif variant == '2':
            p_info("Глупо умер от изнеможения. Смех да и только.")
            break
        else:
            p_info("Зря ты так. Я ведь тебя просил не исполнять")
if __name__ == "__main__":
    main()
#TODO перекинуть все данные в разные файлы + в общий импорт.py. настроить гитигнор. Разобраться с функцией main 