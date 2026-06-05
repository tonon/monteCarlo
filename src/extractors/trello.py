import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from .base import BaseExtractor

load_dotenv()

class TrelloExtractor(BaseExtractor):
    def __init__(self):
        self.api_key = os.getenv("TRELLO_API_KEY")
        self.token = os.getenv("TRELLO_TOKEN")
        self.board_id = os.getenv("TRELLO_BOARD_ID")
        self.base_url = "https://api.trello.com/1"

    def fetch_board_data(self):
        # Busca listas (colunas)
        lists_url = f"{self.base_url}/boards/{self.board_id}/lists"
        params = {'key': self.api_key, 'token': self.token}
        lists = requests.get(lists_url, params=params).json()
        list_name = {lst['id']: lst['name'] for lst in lists}

        # Busca cards
        cards_url = f"{self.base_url}/boards/{self.board_id}/cards"
        params['fields'] = 'id,name,idList,dateLastActivity,closed'
        cards = requests.get(cards_url, params=params).json()

        rows = []
        for card in cards:
            dt_done = None
            if card.get('closed'):
                dt_done = datetime.strptime(card['dateLastActivity'], "%Y-%m-%dT%H:%M:%S.%fZ")
            rows.append({
                '_id': card['id'],
                'name': card['name'],
                'lane': list_name.get(card['idList'], 'unknown'),
                'coluna_kanban': list_name.get(card['idList'], 'unknown'),
                'dtDone': dt_done,
                'createdAt': None,  # Trello não fornece criação fácil
                'card_type': 'task'
            })
        return pd.DataFrame(rows)