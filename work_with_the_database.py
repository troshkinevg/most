import peewee


class DatabaseUpdater:

    def __init__(self, directory, three_days=None):
        self.directory = directory
        self.three_days = three_days
        self.database = peewee.SqliteDatabase(self.directory)
        self.days = []

    def new_create(self):
        class BaseTable(peewee.Model):
            class Meta:
                database = self.database

        class WeatherForecasts(BaseTable):
            date = peewee.DateField()
            weather = peewee.CharField()
            temperature = peewee.CharField()

        return WeatherForecasts

    def create_new_database(self):
        self.database.create_tables([self.new_create()])

    def write_to_database(self, day):
        self.new_create().create(date=day['date'],
                                 weather=day['weather'],
                                 temperature=day['temperature'])
