from pages.page import Page


class DashboardPage(Page):
    def __init__(self):
        super().__init__()
                
        self.layout().addStretch()