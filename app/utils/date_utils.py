from datetime import datetime, date, timedelta


class Delta:
    def __init__(self):
        self.utc_now = datetime.utcnow()
        self.timedelta = 0

    @classmethod
    def datetime_after_hours(cls, diff: int = 0) -> datetime:
        return (
            cls().utc_now + timedelta(hours=diff)
            if diff > 0
            else cls().utc_now + timedelta(hours=diff)
        )

    @classmethod
    def date(cls, diff: int = 0) -> date:
        return cls.datetime(diff=diff).date()

    @classmethod
    def date_num(cls, diff: int = 0) -> int:
        return int(cls.date(diff=diff).strftime("%Y%m%d"))
