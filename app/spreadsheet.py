import os
from typing import List, Type, Optional
import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError
from settings import settings
from models import Order, BaseModel


class SpreadSheet():

    def __init__(self, model: Type[BaseModel], spreadsheet_id: str=None, sheet_id: str='list1'):
        self.spreadsheet_id = spreadsheet_id or settings.SHEET_ID
        self.sheet_id = sheet_id
        self.model = model

    def _get_service_sacc(self):
        creds_json = os.path.dirname(__file__) + settings.TOKEN_FILE_PATH
        scopes = ['https://www.googleapis.com/auth/spreadsheets']

        creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
        return build('sheets', 'v4', http=creds_service)

    def get_rows(self, rows: str=None) -> List[Type[BaseModel]]:
        query = f'{self.sheet_id}' + f'!{rows}' if rows else f'{self.sheet_id}'
        try:
            data = self._get_service_sacc().spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range=query).execute()
        except HttpError as err:
            print(err)
            return []
        return [self.model(*row) for row in data['values'][1:]]

orderSheet = SpreadSheet(Order)