class Menu:
    menu_pages = [
        '/bme280-hourly/humidity',
        '/bme280-hourly/pressure',
        '/bme280-hourly/temperature',
        '/',
        '/bme280-weekly/temperature',
        '/bme280-weekly/pressure',
        '/bme280-weekly/humidity',
    ]

    def __init__(self):
        pass

    def get(self, url):
        total = len(self.menu_pages)
        index = self.menu_pages.index(url)
        previous_index = index - 1
        if previous_index < 0:
            previous_index = total - 1
        next_index = index + 1
        if next_index > total - 1:
            next_index = 0
        menu = {
            'menu': self.menu_pages,
            'total': total,
            'current': url,
            'current_id': index,
            'previous': self.menu_pages[previous_index],
            'next': self.menu_pages[next_index]
        }
        return menu
