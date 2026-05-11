# infrastructure/excel/excel_risk_repository.py

import pandas as pd
from database.base import RiskRepository


class ExcelRiskRepository(RiskRepository):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def _read(self):
        return pd.read_excel(self.file_path)

    def _write(self, df):
        df.to_excel(self.file_path, index=False)

    def get_all(self):
        df = self._read()
        return df.to_dict(orient="records")

    def get_by_id(self, risk_id: int):
        df = self._read()

        row = df[df["ID"] == risk_id]

        if row.empty:
            return None

        return row.iloc[0].to_dict()

    def create(self, risk_data: dict):
        df = self._read()

        df = pd.concat([
            df,
            pd.DataFrame([risk_data])
        ], ignore_index=True)

        self._write(df)

        return risk_data