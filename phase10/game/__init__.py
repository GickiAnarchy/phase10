


from json import JSONEncoder

class Phase10Encoder(JSONEncoder):
    def default(self, o):
        msg = {}
        if type(o) == "Player":
            msg = {"name":o.name,
            "hand":o.hand,
            "score":o.score,
            "current_phase":o.current_phase,
            "win":o.win,
            "is_skipped":o.is_skipped,
            "is_active":o.is_active,
            "current_turn_step":o.current_turn_step,
            "player_id":o.player_id,
            "pin":o.pin}

        if type(o) == "Card":
            msg = {"id":o.id,
            "number":o.number,
            "color":o.is_skip,
            "is_skip":o.color,
            "is_wild":o.is_wild,
            "image":o.image}

        if type(o) == "Phase":
            msg = {"name":o.name,
            "number":o.number,
            "goals":o.goals,
            "complete":o.complete}

        if type(o) == "Goal":
            msg = {
            "min_cards":o.min_cards,
            "cards":o.cards,
            "name":o.name,
            "complete":o.complete,
            "g_type":o.g_type,
            "goal_id":o.goal_id
            }

        if type(o) == "Deck":
            msg = {"cards":o.cards}

        if type(o) == "Discards":
            msg = {"cards":o.cards,
            "image":o.image}

        return msg