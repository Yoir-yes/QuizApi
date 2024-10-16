from PyQt6.QtWidgets import QDialog, QRadioButton, QSizePolicy, QMessageBox

from ApiHandler import ApiHandler
from Question import Question
from question_layout import Ui_Question


class Questions(QDialog):
    def __init__(self, category:str, limit:int):
        super().__init__()
        self.number_of_questions = 0
        self.score = 0
        self.buttons = []
        self.ui = Ui_Question()
        self.ui.setupUi(self)
        self.questions = ApiHandler.getQuestions(category,limit)
        self.get_questions(self.questions[0])
        self.ui.nextbutton.clicked.connect(self.next_question)
        self.show()

    def get_questions(self, question: Question):
        self.ui.questionLabel.setText(question.question_text)

        for button in self.buttons:
            self.ui.verticalLayout.removeWidget(button)
        self.buttons = []

        for answer in question.answer:
            button = QRadioButton(question.question_text)
            button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            self.buttons.append(button)

        for button in self.buttons:
            self.ui.verticalLayout.addWidget(button)

    def get_checked_button(self):
        for i, button in  enumerate(self.buttons):
            if button.isChecked():
                return i
            return None

    def next_question(self):
        if self.get_checked_button() == self.questions[self.number_of_questions].correct_answer:
            self.score += 1


        self.number_of_questions += 1
        if self.number_of_questions <= len(self.questions):
            self.get_questions(self.questions[self.number_of_questions - 1])

        if self.number_of_questions + 1 == len(self.questions):
            msgBox = QMessageBox()
            msgBox.setText("Twój wynik to: "+ str(self.score))
            msgBox.show()
            msgBox.exec()


