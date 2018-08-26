from pymongo import MongoClient
from pymongo.collection import ReturnDocument

client = MongoClient('mongodb://localhost:27017/')
db = client['ashoka-bot']
menus = db.menus

# menu = {
# 	"meal": "lunch",
# 	"menu": {
# 		"everyday": ['a', 'b', 'c'],
# 		"monday": ['d', 'e'],
# 		"tuesday": ['f', 'g']
# 	}
# }

menu_id = menus.find_one_and_update(
	{
		"meal": "lunch"
	},
	{
		"$set": {
			"menu.everyday": ['x', 'y', 'z']
		}
	},
	return_document = ReturnDocument.AFTER,
	upsert = False
)

print menu_id

client.close()