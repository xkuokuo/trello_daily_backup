import json
import requests

from entity import BoardSummary, ListSummary, CardSummary, Card

API_URL="https://api.trello.com/"

class ApiAdapter:
    """Yeah just an trello api adapter"""
    def __init__(self, credential_provider):
        self.access_key = credential_provider.get_access_key()
        self.token = credential_provider.get_token();

    def list_boards(self):
        res = requests.get("{}1/members/me/boards?key={}&token={}".format(
            API_URL,
            self.access_key,
            self.token))
        boards_json = json.loads(res.content)
        boards = []
        for e in boards_json:
            boards.append(BoardSummary(e['name'], e['id']))
        return boards


    def get_board(self, board_id):
        res = requests.get("{}/1/boards/{}/?fields=all&key={}&token={}".format(
            API_URL,
            board_id,
            self.access_key,
            self.token))
        board_json = json.loads(res.content)
        return BoardSummary(board_json["name"], board_json["id"])


    def list_lists(self, board_id):
        res = requests.get("{}/1/boards/{}/lists?key={}&token={}".format(
            API_URL,
            board_id,
            self.access_key,
            self.token))
        lists = []
        lists_json = json.loads(res.content)
        for e in lists_json:
            lists.append(ListSummary(e['name'], e['id']))
        return lists

    def list_cards(self, list_id):
        res = requests.get("{}/1/lists/{}/cards?key={}&token={}".format(
            API_URL,
            list_id,
            self.access_key,
            self.token))
        cards = []
        cards_json= json.loads(res.content)
        for e in cards_json:
            cards.append(Card(e['name'], e['desc']))
        return cards

    def add_card(self, list_id, card_name, desc=""):
        res = requests.post("{}1/cards?idList={}&name={}&desc={}&keepFromSource=all&key={}&token={}".format(
            API_URL,
            list_id,
            card_name,
            desc,
            self.access_key,
            self.token))
        if res.status_code == requests.codes.ok:
            return True
        else:
            print("Error status code: {}".format(res.status_code))
            print(res.content)
            return False;

    def get_card(self, card_id):
        res = requests.get("{}/1/cards/{}?key={}&token={}".format(
            API_URL,
            card_id,
            self.access_key,
            self.token))
        if res.status_code == requests.codes.ok:
            card_json = json.loads(res.content)
            return Card(card_json['name'], card_json['desc'])
        else:
            raise Exception("Unexpected status code {} when getting card {}".format(res.status_code, card_id))

