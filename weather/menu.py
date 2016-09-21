class Menu:
    menu_pages = [
        '/bme280-averaged/humidity',
        '/bme280-averaged/pressure',
        '/bme280-averaged/temperature',
        '/',
        '/bme280-high-low/temperature',
        '/bme280-high-low/pressure',
        '/bme280-high-low/humidity',
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
