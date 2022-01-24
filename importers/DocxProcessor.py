class DocxProcessor:
    def __init__(self):
        # super().__init__()

        self.lstQuestions = []
        self.lstAnswers = []
        # Read in text file
        with open("trivia.txt") as fp:
            lines = fp.readlines()
            for line in lines:
                # print(f'CHECKING LINE:{line}')
                # if line[0].isalpha():

                import re
                # CATEGORY CHECK
                if re.search('^[A-Z][a-z]', line):
                    # print(f'CATEGORY:{line}')
                    self.updateCategory(line)

                # BLANK LINE CHECK
                if line.isspace():
                    # print('BLANK LINE')
                    continue

                # QUESTION CHECK
                if line[0].isdigit():
                    # QUESTION, Display it
                    # print(f'QUESTION:{line}')
                    self.updateQuestion(line)

                # ANSWER CHECK
                if re.search('^\\t+[A-Z]*', line):
                    # print(f'ANSWER:{line}')
                    self.addAnswerToList(line.strip())

    def updateCategory(self, category):
        print(f'Updating Category to {category}')

    def updateQuestion(self, question):
        self.lstQuestions.append(question)
        print(f'Updating Question to {question}')

    def addAnswerToList(self, answer):
        self.lstAnswers.append(answer)
        print(f'Adding answer {answer}')


if __name__ == "__main__":
    app = DocxProcessor()
