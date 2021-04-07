### Running
Run base_bot/code.py
### about files
values in base_bot/values.py
class defs is like client bot better
class user for users in bot
class room is server when play game
class card_info read data from sql and show (this class help you for show card infos)
server_list.txt is show servers in runing
library have def for help you
test.py is for test funcs or code
lib files is sorosh client and examples
### user.*
Class user have this:

user.ID     : Id user for send messge and keyboards
user.name   : User's name
user.amtiaz : Indicates the user scores
user.uadmin : Indicates the user access level (Dfault is "Normal")
user.tdavat : Shows the number of people invited by this user
user.tcoin  : Indicates the number of user coins}

### room.*
Class room have this:

room.number       : number
room.user_id      : Id user for send messge and keyboards
room.cards        : Show him cards
room.create_cards : Show him create_cards
room.coins        : Show him coins
room.karakter_one : Show karakter (first )
room.karakter_two : Show karakter (second)

### card_info.*
Class card_info have this:

card_info.card_id   : This primary key
card_info.card_name : Show Name
card_info.owner     : Show good karakter for this card
card_info.buy       : Indicates the coins needed to build
card_info.plus      : Shows additional capabilities

### This program is not compelet