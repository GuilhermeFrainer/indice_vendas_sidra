import datetime


class Index:
    
    def __init__(self, date, retail, ext_retail, industry, services):
        
        self.date = date
        self.retail = retail
        self.ext_retail = ext_retail
        self.industry = industry
        self.services = services

    @property
    def date(self):
        return self._date

    # Expects date in the yyyymm format
    @date.setter
    def date(self, date):
        
        month = date[4:]
        year = date[:4]

        self._date = datetime.date.fromisoformat(f"{year}-{month}-01")