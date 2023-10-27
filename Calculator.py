# -*- coding: utf8 -*-

from re import search
from tkinter import BOTH, TOP, Button, E, Event, Frame, Label, StringVar, Tk

from Operation import Operation

"""
電卓クラス
"""


class Calculator(Tk):
    """

    電卓クラス

    """

    # 整数部の桁数
    INTEGER_DIGITS = 12

    # 小数部の桁数
    DECIMAL_DIGITS = 3

    def __init__(self):
        """

        コンストラクター

        """
        super().__init__()

        # 変数の初期化
        self.clear()
        self.clearMemory()

        # コントロールのフォント
        fontName: str = "meiryo"

        # タイトル
        self.title("電卓")

        # 式と計算結果のフレーム
        displayFlame: Frame = Frame(self)
        displayFlame.pack(side=TOP, fill=BOTH, padx=10)

        # 式
        self.formulaStringVar: StringVar = StringVar()
        Label(
            displayFlame,
            textvariable=self.formulaStringVar,
            font=(fontName, 15),
            anchor=E,
        ).pack(side=TOP, fill=BOTH)

        # 計算結果
        self.inputStringVar: StringVar = StringVar()
        self.inputLabel: Label = Label(
            displayFlame,
            textvariable=self.inputStringVar,
            font=(fontName, 21),
            anchor=E,
        )

        self.inputLabel.pack(side=TOP, fill=BOTH)

        # ボタンのフレーム
        buttonFrame = Frame(self)
        buttonFrame.pack(side=TOP, padx=2, pady=2)

        # ボタン
        buttonTexts: list[list[str]] = [
            ["MR", "M+", "M-", "MS"],
            ["MC", "CE", "C", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["+/-", "0", ".", "="],
        ]
        for buttonTextsRow in buttonTexts:
            for buttonText in buttonTextsRow:
                button: Button = Button(
                    buttonFrame,
                    text=buttonText,
                    font=(fontName, 15),
                    width=6,
                    height=1,
                )
                row = buttonTexts.index(buttonTextsRow)
                column = buttonTextsRow.index(buttonText)
                button.grid(row=row, column=column, padx=1, pady=1)

                # ボタン押下時の処理を設定
                button.bind("<Button-1>", self.buttonClicked)

        # キーボード押下時の処理
        self.bind("<KeyPress>", self.keyPressed)

        # ラベルを描画
        self.redraw()

    def buttonClicked(self, event: Event):
        """

        ボタン押下時の処理

        Args:
            event Event: イベント
        """
        buttonText = event.widget["text"]
        if self.isErrorOccurred and buttonText != "C":
            # エラー時はクリア以外不可
            return

        if buttonText == "+":
            self.inputOperation(Operation.ADDITION)
        elif buttonText == "-":
            self.inputOperation(Operation.SUBTRACT)
        elif buttonText == "*":
            self.inputOperation(Operation.MULTIPLICATION)
        elif buttonText == "/":
            self.inputOperation(Operation.DIVISION)
        elif buttonText == "=":
            self.inputOperation(Operation.EQUAL)
        elif buttonText == ".":
            self.inputDecimalPoint()
        elif buttonText == "+/-":
            self.changePlusMinus()
        elif buttonText == "C":
            self.clear()
        elif buttonText == "CE":
            if self.lastOperation == Operation.EQUAL:
                # イコール押下時はクリアーと同じ処理を行う
                self.clear()
            else:
                self.clearEntry()
        elif buttonText == "MR":
            self.callMemory()
        elif buttonText == "M+":
            self.addMemory()
        elif buttonText == "M-":
            self.subtractMemory()
        elif buttonText == "MS":
            self.saveMemory()
        elif buttonText == "MC":
            self.clearMemory()
        else:
            # 数字
            self.inputNumber(int(buttonText))

        self.redraw()

    def keyPressed(self, event: Event):
        """

        キーボード押下時の処理

        Args:
            event Event: イベント
        """
        pressedKey: str = event.keysym
        if self.isErrorOccurred and pressedKey != "Escape":
            # エラー時はクリア以外不可
            return

        if pressedKey == "plus":
            self.inputOperation(Operation.ADDITION)
        elif pressedKey == "minus":
            self.inputOperation(Operation.SUBTRACT)
        elif pressedKey == "asterisk":
            self.inputOperation(Operation.MULTIPLICATION)
        elif pressedKey == "slash":
            self.inputOperation(Operation.DIVISION)
        elif pressedKey == "Return":
            self.inputOperation(Operation.EQUAL)
        elif pressedKey == "period":
            self.inputDecimalPoint()
        elif pressedKey == "Escape":
            self.clear()
        elif pressedKey in map(lambda x: str(x), range(10)):
            self.inputNumber(int(pressedKey))

        self.redraw()

    def inputNumber(self, number: int):
        """

        数字入力

        Args:
            number int: 入力された数字
        """
        if self.lastOperation == Operation.EQUAL:
            # イコール押下直後は初期化する
            self.clear()

        if self.isDecimalPointInput:
            # 小数
            if number == 0:
                # 小数点以下のゼロは数値的に変化しないため回数を覚えておく
                self.decimalZeroCount += 1
                return

            # 小数部の桁数を数える
            strInput: str = str(self.input)
            decimalPart: str = search(r"\..+", strInput).group()

            # 小数点が含まれるため-1
            decimalDigits: int = len(decimalPart) - 1
            if decimalDigits >= self.DECIMAL_DIGITS:
                # 対応桁数を超えたため何もしない
                return

            if self.isInteger(self.input):
                # 整数(小数点押下直後)
                decimalDigits = 0

            addNumber: float = number
            for x in range(decimalDigits + 1 + self.decimalZeroCount):
                addNumber /= 10

            self.input += addNumber

            # 稀に誤差が発生するため四捨五入
            self.input = round(self.input, self.DECIMAL_DIGITS)

            self.decimalZeroCount = 0
        else:
            # 整数
            # 整数部の桁数を数える
            strInput: str = str(self.input)
            integerPart: str = search(r".+\.", strInput).group()

            # 小数点が含まれるため-1
            if len(integerPart) - 1 >= self.INTEGER_DIGITS:
                # 対応桁数を超えたため何もしない
                return

            self.input = self.input * 10 + number

    def inputOperation(self, operation: Operation):
        """

        四則演算、イコールの押下

        Args:
            operation Operation: 入力された命令
        """
        # イコール押下時は表示用に計算式を覚えておく
        if (
            operation == Operation.EQUAL
            and self.lastOperation != Operation.EQUAL
        ):
            strInput: str = str(self.input)
            if self.isInteger(self.input):
                # 整数の場合は小数点以下を非表示
                strInput = str(int(self.input))
            self.previousFormula = self.formulaStringVar.get() + strInput + "="

        # 計算
        if self.lastOperation == Operation.INITIAL:
            self.result = self.input
        elif self.lastOperation == Operation.ADDITION:
            self.result += self.input
        elif self.lastOperation == Operation.SUBTRACT:
            self.result -= self.input
        elif self.lastOperation == Operation.MULTIPLICATION:
            self.result *= self.input
        elif self.lastOperation == Operation.DIVISION:
            if self.input == 0:
                self.isErrorOccurred = True
                self.errorMessage = "0で割った"
            else:
                self.result /= self.input
        elif self.lastOperation == Operation.EQUAL:
            pass
        else:
            raise Exception("不明なOperationです")

        # 桁数が有効範囲を超えている場合はエラーもしくは四捨五入
        self.result = round(self.result, self.DECIMAL_DIGITS)
        if (
            self.result >= 10**self.INTEGER_DIGITS
            or self.result <= -1 * 10**self.INTEGER_DIGITS
        ):
            self.isErrorOccurred = True
            self.errorMessage = f"整数部が{self.INTEGER_DIGITS}桁を超えた"

        # 命令を記憶して入力を初期化
        self.lastOperation = operation
        self.clearEntry()

    def inputDecimalPoint(self):
        """

        小数点入力

        """
        if self.lastOperation == Operation.EQUAL:
            # イコール押下直後は初期化する
            self.lastOperation = Operation.INITIAL

        # 小数点入力済みの場合は何もしない
        if not self.isDecimalPointInput:
            self.isDecimalPointInput = True

    def changePlusMinus(self):
        """

        入力値の正負を逆転する

        """
        if self.lastOperation == Operation.EQUAL:
            # イコール押下直後は初期化する
            self.lastOperation = Operation.INITIAL

        self.input *= -1

    def clear(self):
        """クリアー

        各変数を初期化

        """
        self.lastOperation: Operation = Operation.INITIAL
        self.previousFormula: str = ""
        self.result: float = 0.0
        self.isErrorOccurred: bool = False
        self.errorMessage: str = ""
        self.clearEntry()

    def clearEntry(self):
        """

        入力を初期化

        """
        # 小数点が入力されたか
        self.isDecimalPointInput: bool = False

        # 小数点以下で0を入力した回数
        self.decimalZeroCount: int = 0

        # 入力と計算結果
        self.input: float = 0.0

    def callMemory(self):
        """

        メモリー呼び出し

        """
        if self.lastOperation == Operation.EQUAL:
            # イコール押下直後は初期化する
            self.lastOperation = Operation.INITIAL

        self.input = self.memory

    def clearMemory(self):
        """

        メモリークリア

        """
        self.memory = 0.0

    def saveMemory(self):
        """

        メモリー保存

        """
        input: float = self.input
        if self.lastOperation == Operation.EQUAL:
            # イコール押下直後は計算結果を使用
            input = self.result

        self.memory = input

    def addMemory(self):
        """

        メモリー加算

        """
        input: float = self.input
        if self.lastOperation == Operation.EQUAL:
            # イコール押下直後は計算結果を使用
            input = self.result

        self.memory += input
        if (
            self.memory >= 10**self.INTEGER_DIGITS
            or self.memory <= -1 * 10**self.INTEGER_DIGITS
        ):
            self.clearMemory()
            self.isErrorOccurred = True
            self.errorMessage = f"メモリーが{self.INTEGER_DIGITS}桁を超えた"

    def subtractMemory(self):
        """

        メモリー減算

        """
        input: float = self.input
        if self.lastOperation == Operation.EQUAL:
            # イコール押下直後は計算結果を使用
            input = self.result

        self.memory -= input
        if (
            self.memory >= 10**self.INTEGER_DIGITS
            or self.memory <= -1 * 10**self.INTEGER_DIGITS
        ):
            self.clearMemory()
            self.isErrorOccurred = True
            self.errorMessage = f"メモリーが{self.INTEGER_DIGITS}桁を超えた"

    def redraw(self):
        """

        再描画

        """
        # エラー
        if self.isErrorOccurred:
            self.inputStringVar.set(self.errorMessage)
            self.formulaStringVar.set("")
            return

        # 計算結果
        formula: str = ""
        result: float = self.result
        if self.isInteger(self.result):
            # 整数の場合は小数点以下を非表示
            result = int(self.result)

        strResult: str = str(result)
        if self.lastOperation == Operation.INITIAL:
            pass
        elif self.lastOperation == Operation.ADDITION:
            formula = strResult + "+"
        elif self.lastOperation == Operation.SUBTRACT:
            formula = strResult + "-"
        elif self.lastOperation == Operation.MULTIPLICATION:
            formula = strResult + "*"
        elif self.lastOperation == Operation.DIVISION:
            formula = strResult + "/"
        elif self.lastOperation == Operation.EQUAL:
            formula = self.previousFormula
            self.input = self.result
        else:
            raise Exception("不明なOperationです")

        # 入力
        input: float = self.input
        if self.isInteger(self.input):
            # 整数の場合は小数点以下を非表示
            input = int(self.input)

        # 小数点以下のゼロに対応
        strInput: str = f"{input:,}"
        for x in range(self.decimalZeroCount):
            strInput += "0"

        # 描画
        self.inputStringVar.set(strInput)
        self.formulaStringVar.set(formula)

    def isInteger(self, number: float) -> bool:
        """

        数値が整数か判定

        Args:
            number float: 判定する数値

        Returns:
            bool: 整数であればTrue
        """
        return number == int(number)
