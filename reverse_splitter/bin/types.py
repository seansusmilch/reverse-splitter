from dataclasses import dataclass
from typing import Optional

@dataclass
class Split:
    ticker: str
    exchange: str
    company_name: str
    ratio: str
    effective_date: str
    
    press_release_url: Optional[str] = None
    summary: Optional[str] = None
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Split):
            return False
        
        return self.ticker == value.ticker
    
    def __hash__(self) -> int:
        return hash(self.ticker)

if __name__ == '__main__':
    spl2 = Split('RYAAY', 'NASDAQ', 'Ryanair Holdings plc', '5:2', '2024-09-30')
    spl1 = Split('RYAAY', 'NAS', 'ddd', '52', '2024--30')
    spl4 = Split('RYAAY', 'NAS', 'dfasdfsd', '5asdfasdf2', 'asdfasdf--30')
    spl3 = Split('RYAAY', 'NasdfasdfasdfAS', '', '52', '2024--30asdf')
    
    dedupe = {spl1, spl2, spl3, spl4}
    dedupe1 = {spl1, spl2, spl3, spl4}
    dedupe2 = {spl1, spl2, spl3, spl4}
    print(dedupe)
    print(len(dedupe))
    
    