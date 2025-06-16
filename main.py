from dataclasses import dataclass, field
from enum import Enum, auto
from random import randint, choice
import logging

#Нужно выполнить задание по логгированию, добавить макс хп, перемещение по локациям, инвентарь и получение предметов, восстановление здоровья, шансы побега.
#class Main(Enum):
class Area(Enum):
    plain  =    auto()
    forest =    auto()
    mountain =  auto()
    swamps =    auto()
    ruins  =    auto()

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
        logging.debug(f"Бедный моб погиб")
@dataclass
class Player():
    name: str
    lvl: int
    #max_hp = 100
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
            logging.info(f"Поздравляем с получением {self.lvl} уровня")       
def main():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('battle.log')
    file_handler.setFormatter(logging.Formatter('%(message)s'))
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    player = Player("Игрок", 1, 100)
    found_enemy  = Enemy(choice(area_enemy[player.location]), choice(area_lvl[player.location]), 100)
    def new_enemy():
        del found_enemy
        logging.critical("Пытаемся удалить врага")
        found_enemy  = Enemy(choice(area_enemy[player.location]), choice(area_lvl[player.location]), 100)
    def set_player_name(name):
        if name:
            player.name = name
            logging.info(f"Понятно. Очередной {player.name}")
        else:
            player.name = "Игрок"
            logging.info("Тогда будешь стандартным Игроком\n")
    def combat(player: Player, found_enemy  : Enemy) -> str:
        while player.hp > 0 and found_enemy.hp > 0:
            player_dmg = player.damage()
            enemy_dmg = found_enemy.damage()
            player.hp -= enemy_dmg
            found_enemy.hp -= player_dmg
            logging.info(f"{player.name} Уебал {found_enemy.name} на {player_dmg} единиц урона. Но получил ответку на {enemy_dmg} единиц урона по лицу")
            if player.hp <= 0:
                logging.info("Йоу, ты умер.")
                return "dead"
            elif found_enemy.hp <= 0:
                logging.info("Туда его. Красава! Завалил гниду.")
                return "win"
            else:    
                logging.info(f"У вас осталось {player.hp} здоровья. У вражины {found_enemy .hp}.Что делаем?\n 1 - сражайся как мужчина\n 2 - в ужасе сьеби в туман")
                fight_choise = input()
                if fight_choise == '1':
                    logging.info("Продолжаем файт")
                #TODO Стоит добавить шанс на побег. *В следующих версиях
                elif fight_choise == '2':
                    logging.info("Ты тут вообще то в сражении. Развернувшись ты тут же получил удра в хребет и умер. Лошара")
                    return "dead"
                else:
                    logging.info("Ты что, тупой? Выбирай нормально")
                             
    logging.info(f"Привет! Сегодня ты возьмешь на себя роль беттатестера угрюмой хуеты, которая может стать игрой. Выбора особого у тебя конечно же нет.")
    name_p =  input("Ну что дружище, как звать то тебя?\n")
    set_player_name(name_p)
    #Внезапная генерация врага
    logging.info(f"""Ты оказался на равнинах, вокруг раскинулись луга. Ляпота.
Внезапно!
Ты встречаешь {found_enemy .name}
Так как вариантов у тебя немного, оставляю тебе 2 выбора:
Вариант 1 - ты сражаешься
Вариант 2 - ты умираешь от голода""")
    while True:
        variant = input("Выбирай с умом. И не надо лишнего. Либо 1, либо 2.\n")
        if variant == '1':
            logging.info("Ну давай, заебашь его")
            buttle_result = combat(player, found_enemy)
            if buttle_result == "dead":
                logging.info("Записали тебя в позорники")
                return 0
            elif buttle_result == "win":
                logging.info("Ай Маладец!")
                logging.info(f"Вы получили {found_enemy .give_exp} опыта")
                player.try_lvl_up(found_enemy .give_exp)
                return 0
            else:
                logging.info("Попытайся снова")
        elif variant == '2':
            logging.info("Глупо умер от изнеможения. Смех да и только.")
            break
        else:
            logging.info("Зря ты так. Я ведь тебя просил не исполнять")
if __name__ == "__main__":
    main()
