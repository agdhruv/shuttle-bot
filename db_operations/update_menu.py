# save menu in db when received
def update_menu_in_db(received_dict):
    from pymongo.collection import ReturnDocument
    from connect import connect
    import os

    client = connect(os.environ["MONGODB_URI"] if os.environ.get("MONGODB_URI") else "mongodb://localhost:27017/ashoka-bot")
    db = client.get_default_database()

    updated_document = db.menus.find_one_and_update(
        {
            'meal': received_dict['meal']
        },
        {
            '$set': {
                'menu': received_dict['menu'],
                'timings': received_dict['timings']
            }
        },
        projection = {
            '_id': False
        },
        return_document = ReturnDocument.AFTER,
        upsert = False
    )

    client.close()

    return updated_document