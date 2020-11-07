def __init__(self):
    self.url = 'https://mariamingallonmm.github.io/AI-SearchAlgorithm-A2-2048puzzle/'
    self.driver = webdriver.Chrome(ChromeDriverManager().install())  # Optional argument, if not specified will search path.
    self.driver.get(self.url)
    self.body = self.driver.find_element_by_tag_name('body')
    self.moves = {
        0: Keys.ARROW_UP,
        1: Keys.ARROW_DOWN,
        2: Keys.ARROW_LEFT,
        3: Keys.ARROW_RIGHT
    }
