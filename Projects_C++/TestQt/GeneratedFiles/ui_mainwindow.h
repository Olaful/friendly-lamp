/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.11.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QToolButton>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QAction *actionenjoy;
    QWidget *centralWidget;
    QLabel *label;
    QToolButton *toolButton_1;
    QToolButton *toolButton_2;
    QTextEdit *textEdit_1;
    QLabel *label_2;
    QLabel *label_3;
    QLabel *label_4;
    QLineEdit *lineEdit_1;
    QLineEdit *lineEdit_2;
    QLabel *label_5;
    QLineEdit *lineEdit_3;
    QLabel *label_6;
    QLineEdit *lineEdit_4;
    QToolButton *toolButton_3;
    QToolButton *toolButton_4;
    QTextEdit *textEdit_2;
    QMenuBar *menuBar;
    QMenu *menu;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(667, 476);
        actionenjoy = new QAction(MainWindow);
        actionenjoy->setObjectName(QStringLiteral("actionenjoy"));
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        label = new QLabel(centralWidget);
        label->setObjectName(QStringLiteral("label"));
        label->setGeometry(QRect(133, 120, 51, 31));
        QFont font;
        font.setFamily(QStringLiteral("Adobe Arabic"));
        font.setPointSize(18);
        font.setBold(true);
        font.setWeight(75);
        label->setFont(font);
        toolButton_1 = new QToolButton(centralWidget);
        toolButton_1->setObjectName(QStringLiteral("toolButton_1"));
        toolButton_1->setGeometry(QRect(200, 125, 51, 21));
        toolButton_1->setStyleSheet(QStringLiteral(""));
        toolButton_2 = new QToolButton(centralWidget);
        toolButton_2->setObjectName(QStringLiteral("toolButton_2"));
        toolButton_2->setGeometry(QRect(270, 125, 51, 21));
        textEdit_1 = new QTextEdit(centralWidget);
        textEdit_1->setObjectName(QStringLiteral("textEdit_1"));
        textEdit_1->setGeometry(QRect(200, 80, 104, 21));
        label_2 = new QLabel(centralWidget);
        label_2->setObjectName(QStringLiteral("label_2"));
        label_2->setGeometry(QRect(140, 74, 51, 31));
        label_2->setFont(font);
        label_3 = new QLabel(centralWidget);
        label_3->setObjectName(QStringLiteral("label_3"));
        label_3->setGeometry(QRect(134, 160, 51, 31));
        label_3->setFont(font);
        label_4 = new QLabel(centralWidget);
        label_4->setObjectName(QStringLiteral("label_4"));
        label_4->setGeometry(QRect(250, 160, 16, 31));
        label_4->setFont(font);
        lineEdit_1 = new QLineEdit(centralWidget);
        lineEdit_1->setObjectName(QStringLiteral("lineEdit_1"));
        lineEdit_1->setGeometry(QRect(200, 167, 41, 20));
        lineEdit_1->setStyleSheet(QStringLiteral(""));
        lineEdit_2 = new QLineEdit(centralWidget);
        lineEdit_2->setObjectName(QStringLiteral("lineEdit_2"));
        lineEdit_2->setGeometry(QRect(270, 166, 41, 20));
        label_5 = new QLabel(centralWidget);
        label_5->setObjectName(QStringLiteral("label_5"));
        label_5->setGeometry(QRect(321, 160, 16, 31));
        label_5->setFont(font);
        lineEdit_3 = new QLineEdit(centralWidget);
        lineEdit_3->setObjectName(QStringLiteral("lineEdit_3"));
        lineEdit_3->setGeometry(QRect(340, 166, 41, 20));
        label_6 = new QLabel(centralWidget);
        label_6->setObjectName(QStringLiteral("label_6"));
        label_6->setGeometry(QRect(391, 160, 16, 31));
        label_6->setFont(font);
        lineEdit_4 = new QLineEdit(centralWidget);
        lineEdit_4->setObjectName(QStringLiteral("lineEdit_4"));
        lineEdit_4->setGeometry(QRect(410, 166, 41, 20));
        toolButton_3 = new QToolButton(centralWidget);
        toolButton_3->setObjectName(QStringLiteral("toolButton_3"));
        toolButton_3->setGeometry(QRect(132, 200, 51, 21));
        toolButton_3->setStyleSheet(QStringLiteral(""));
        toolButton_4 = new QToolButton(centralWidget);
        toolButton_4->setObjectName(QStringLiteral("toolButton_4"));
        toolButton_4->setGeometry(QRect(193, 200, 51, 21));
        toolButton_4->setStyleSheet(QStringLiteral(""));
        textEdit_2 = new QTextEdit(centralWidget);
        textEdit_2->setObjectName(QStringLiteral("textEdit_2"));
        textEdit_2->setGeometry(QRect(135, 230, 104, 111));
        textEdit_2->setLineWrapMode(QTextEdit::WidgetWidth);
        MainWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 667, 23));
        menu = new QMenu(menuBar);
        menu->setObjectName(QStringLiteral("menu"));
        MainWindow->setMenuBar(menuBar);
        mainToolBar = new QToolBar(MainWindow);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        MainWindow->setStatusBar(statusBar);

        menuBar->addAction(menu->menuAction());
        menu->addAction(actionenjoy);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "\344\275\240\345\245\275", nullptr));
        actionenjoy->setText(QApplication::translate("MainWindow", "enjoy", nullptr));
        label->setText(QApplication::translate("MainWindow", "choice:", nullptr));
        toolButton_1->setText(QApplication::translate("MainWindow", "single", nullptr));
        toolButton_2->setText(QApplication::translate("MainWindow", "double", nullptr));
        textEdit_1->setDocumentTitle(QString());
        label_2->setText(QApplication::translate("MainWindow", "test:", nullptr));
        label_3->setText(QApplication::translate("MainWindow", "result:", nullptr));
        label_4->setText(QApplication::translate("MainWindow", "+", nullptr));
        label_5->setText(QApplication::translate("MainWindow", "+", nullptr));
        label_6->setText(QApplication::translate("MainWindow", "=", nullptr));
        toolButton_3->setText(QApplication::translate("MainWindow", "start", nullptr));
        toolButton_4->setText(QApplication::translate("MainWindow", "stop", nullptr));
        textEdit_2->setDocumentTitle(QString());
        menu->setTitle(QApplication::translate("MainWindow", "\350\217\234\345\215\225", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
