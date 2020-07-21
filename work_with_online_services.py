import re
import datetime as dt


class Prediction:
    three_day_temperature = ['/html/body/div[1]/div[2]/div/div/section[1]/div[2]/div/div[1]/div[2]/div/div[3]/span[3]',
                             '/html/body/div[1]/div[2]/div/div/section[1]/div[2]/div/div[2]/div[2]/div/div[3]/span[3]',
                             '/html/body/div[1]/div[2]/div/div/section[1]/div[2]/div/div[3]/div[2]/div/div[3]/span[3]']

    three_day_weather = ['/html/body/div[1]/div[2]/div/div/section[1]/div[2]/div/div[1]/div[2]/div/div[3]/span[2]/i',
                         '/html/body/div[1]/div[2]/div/div/section[1]/div[2]/div/div[2]/div[2]/div/div[3]/span[2]/i',
                         '/html/body/div[1]/div[2]/div/div/section[1]/div[2]/div/div[3]/div[2]/div/div[3]/span[2]/i']

    days = ['/html/body/div[1]/div[2]/div/div/section[1]/div[2]/div/div[1]/div[1]/span',
            '/html/body/div[1]/div[2]/div/div/section[1]/div[2]/div/div[2]/div[1]/span',
            '/html/body/div[1]/div[2]/div/div/section[1]/div[2]/div/div[3]/div[1]/span']

    def __init__(self, html_tree):
        self.html_tree = html_tree
        self.container_days = []

    def new(self):
        for i in range(3):
            box = {}
            nodes = self.html_tree.xpath(self.three_day_temperature[i])
            for node in nodes:
                box['temperature'] = node.text
            units = self.html_tree.xpath(self.three_day_weather[i])
            for unit in units:
                box['weather'] = unit.values()[1]
            d = dt.date.today()
            nodes = self.html_tree.xpath(self.days[i])
            for node in nodes:
                day = re.findall('(\d+)', node.text)[0]
                box['date'] = dt.date(year=d.year, month=d.month, day=int(day))
            self.container_days.append(box)
        return self.container_days
