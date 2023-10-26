# -*- coding: utf8 -*-

from customtkinter import (
    BOTH,
    TOP,
    CTk,
    CTkButton,
    CTkFrame,
    CTkLabel,
    E,
    StringVar,
)

"""
電卓クラス
"""


class Calculator(CTk):
    """

    電卓クラス

    Attributes:
        input (StringVar): 計算結果
        formula (StringVar): 計算式

    """

    def __init__(self):
        """
        コンストラクター
        """
        super().__init__()

        # コントロールのフォント
        font: str = "meiryo"

        # 変数の初期化
        self.input: StringVar = StringVar()
        self.formula: StringVar = StringVar()
        self.clear()

        # タイトル
        self.title("電卓")

        # 式と計算結果のフレーム
        displayFlame: CTkFrame = CTkFrame(self)
        displayFlame.pack(side=TOP, fill=BOTH, padx=2, pady=2)

        # 式
        formulaLabel: CTkLabel = CTkLabel(
            displayFlame,
            textvariable=self.formula,
            font=(font, 15),
            anchor=E,
        )

        # 計算結果
        inputLabel: CTkLabel = CTkLabel(
            displayFlame,
            textvariable=self.input,
            font=(font, 30),
            anchor=E,
        )
        formulaLabel.pack(side=TOP, fill=BOTH, padx=10)
        inputLabel.pack(side=TOP, fill=BOTH, padx=10)

        # ボタンのフレーム
        buttonFrame = CTkFrame(self)
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
                button = CTkButton(
                    buttonFrame,
                    text=buttonText,
                    font=(font, 15),
                    width=80,
                    height=50,
                )
                row = buttonTexts.index(buttonTextsRow)
                column = buttonTextsRow.index(buttonText)
                button.grid(row=row, column=column, padx=1, pady=1)

    def clear(self):
        """
        クリアー
        """
        self.input.set(0.0)
        self.formula.set("testtest")
