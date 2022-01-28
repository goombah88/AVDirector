class Category():
    """A Category is comprised of:
    5 questions,
    5 answers,
    getters and setters?
    """
    # def __init__(self, q1, a1, q2, a2, q3, a3, q4, a4, q5, a5):
    def __init__(self, q1, a1):
        self.q1 = q1
        self.a1 = a1
        # self.q2 = q2
        # self.a2 = a2
        # self.q3 = q3
        # self.a3 = a3
        # self.q4 = q4
        # self.a4 = a4
        # self.q5 = q5
        # self.a5 = a5

    @property
    def q1(self):
        return self.q1

    @q1.setter
    def q1(self, q1):
        self.q1 = q1

    @property
    def a1(self):
        return self.a1

    @a1.setter
    def a1(self, a1):
        self.a1 = a1
