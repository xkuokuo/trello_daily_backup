import threading
from entity import List, Board

class Dao:
    def __init__(self, api):
        self.api = api

    def list_boards(self):
        try:
            board_summaries = self.api.list_boards()
            return board_summaries
        except Exception as e:
            raise Exception(e, "Error Fetching Board Information From Trello XD")

    def list_lists(self, board_id):
        try:
            list_summaries = self.api.list_lists(board_id)
            return list_summaries
        except Exception as e:
            raise Exception(e, "Error Fetching Lists Information For Board ID: {}".format(board_id))

    def list_cards(self, list_id):
        try:
            card_summaries = self.api.list_cards(list_id)
            return card_summaries
        except Exception as e:
            raise Exception(e, "Error Fetching Cards Information For List ID: {}".format(list_id))

    def get_card(self, card_id):
        try:
            card = self.api.get_card(card_id)
            return card
        except Exception as e:
            raise Exception(e, "Error Fetching Card From Card ID: {}".format(card_id))

    def get_board(self, board_id):
        # get lists in board
        try:
            list_summaries = self.api.list_lists(board_id)
            lists = [None] * len(list_summaries)
            threads = []
            for i, l in enumerate(list_summaries):
                # card_summaries = self.api.list_cards(l.list_id)
                # lists.append(List(l.list_name, l.list_id, card_summaries))
                t = threading.Thread(target=self._list_cards_helper, args=(l.list_id, l.list_name, lists, i))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
            board_summary = self.api.get_board(board_id)
            return Board(board_summary.board_name, board_id, lists)
        except Exception as e:
            raise Exception(e, "Error Fetching Board Information From Trello XD")

    def _list_cards_helper(self, list_id, list_name, lists, index):
        cards = self.api.list_cards(list_id)
        lists[index] = List(list_name, list_id, cards)

    def add_card(self, list_id, card_name, desc=""):
        try:
            if not self.api.add_card(list_id, card_name, desc):
                raise Exception("Unexpected status code.")
        except Exception as e:
            raise Exception(e, "Error Adding Card To List")


