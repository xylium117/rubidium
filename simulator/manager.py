import random

import configs.manager as scm


class Manager:
    def __init__(self):
        self.name = random.choice(scm.names)
        self.formation = random.choice(scm.formations)
