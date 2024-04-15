class ScrapeRequestDto:
    def __init__(self,url:str,page:int) -> None:
        self.url = url
        self.page = page
        pass