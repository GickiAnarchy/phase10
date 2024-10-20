"""
Message templates for client/server.
    Message=
        {'type_name':{'client_id':client_id,'key':'value', etc.}}
"""

def get_client_message(message_type:str, client_id:str, game_id:str = None, name:str = None, clients:list = None):
    CLIENT_MESSAGES = {
        "connect":{
            "client_id": "",
            "description":"Client connect"
        },
        "disconnect":{
            "client_id":"Client disconnect"
        },
        "join":{
            "client_id":client_id,
            "game_id":game_id,
            "name":name,
            "description":"Player join game"
        },
        "leave":{
            "client_id":client_id,
            "game_id":game_id,
            "name":name,
            "description":"Player leaves game"
        },
        "load_player":{
            "client_id":client_id,
            "name":name,
            "pin":"",
            "description":"Load player"
        },
        "create_player":{
            "client_id":client_id,
            "name":name,
            "description":"Create player"
        },
        "turn_complete":{
            "client_id":client_id,
            "name":name,
            "description":"Players turn is complete"
        },
        "skipped":{
            "client_id":client_id,
            "description":"Player has turn skipped"
        },
        "draw_deck":{
            "client_id":client_id,
            "name":name,
            "description":"Player draw from deck"
        },
        "draw_discards":{
            "client_id":client_id,
            "name":name,
            "description":"Player draw from discards"
        },
        "play_card":{
            "client_id":client_id,
            "card_id":"",
            "goal_id":"",
            "description":"Plays a card on a goal"
        },
        "play_skip":{
            "client_id":client_id,
            "target_id":"",
            "description":"Player skips target player"
        },
        "discard":{
            "client_id":client_id,
            "card_id":"",
            "description":"Player discards a card"
        },
        "pass":{
            "client_id":client_id,
            "description":"Player passes to discard step"
        },
        "phase_complete":{
            "client_id":client_id,
            "description":"Player completes phase"
        },
        "win":{
            "client_id":client_id,
            "description":"Player wins"
        },
        "deal_cards":{
            "clients":clients,
            "description":"Deal cards to list of client/players"
        }
    }
    return CLIENT_MESSAGES[message_type]
