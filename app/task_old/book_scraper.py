class NaverBookScraper:
    NAVER_API_BOOK = "https://openapi.naver.com/v1/search/book"

    @staticmethod
    def fetch(session, url, headers):
        pass

    def unit_url(self, keyword, start):
        return {"url": f"{self}"}

    def search(self, keyword, total_page):
        apis = [self.unit_url(keyword, 1 + 11 * 10) for i in range(total_page)]
