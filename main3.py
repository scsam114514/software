from PyQt5.QtCore import QTimer, Qt
from LogIn import Ui_LRMainWindow
from testwindow import Ui_testwindow  # 假设testshowmenu.py中定义了Ui_MainWindow类
from mainManufacturerWindow import Ui_ManufacturerWindow
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QFrame, QApplication,QMessageBox,QHBoxLayout,QScrollArea,QPlainTextEdit, QLabel,QMainWindow, QDesktopWidget, QPushButton, QVBoxLayout, QWidget
import sys
import pymysql
import datetime

USERID = None
MANUFACTURERID = None
FLAG = 0 #登录注册的标记

###  adada
num = 10

class LogInWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LRMainWindow()
        self.ui.setupUi(self)

        # 设置窗口无边框及透明背景
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 窗口居中显示
        self.center()

        # 添加退出按钮
        exit_button = QPushButton(self)
        exit_button.setText("X")
        exit_button.setGeometry(QtCore.QRect(self.width() - 50, 10, 40, 40))
        exit_button.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(255, 255, 255, 50);
                        color: white;
                        font: 14pt "微软雅黑";
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 0, 0, 100);
                    }
                """)
        exit_button.clicked.connect(self.close)

        #用户与厂商登陆界面切换
        self.ui.pushButton_switch.clicked.connect(lambda: self.switch_page(FLAG))

        # 按钮绑定函数
        self.ui.pushButton_LogIn.clicked.connect(lambda: self.ui.stackedWidget_LR.setCurrentIndex(FLAG))
        self.ui.pushButton_Register.clicked.connect(lambda: self.ui.stackedWidget_LR.setCurrentIndex(FLAG + 2))

        # 异常栏初始化
        self.ui.success_error_Type.setCurrentIndex(0)

        # 显示登录界面
        self.show()

        # 登录按钮点击事件
        self.ui.pushButton_L_Sure.clicked.connect(lambda :self.log_in(FLAG))
        self.ui.pushButton_L_Sure_manufacturer.clicked.connect(lambda :self.log_in(FLAG))

        #用户与厂商注册按钮点击事件
        self.ui.pushButton_User_R_Sure.clicked.connect(lambda: self.register(FLAG))
        self.ui.pushButton_Manufacturer_R_Sure.clicked.connect(lambda: self.register(FLAG))

    #切换用户/厂商登录
    def switch_page(self, pageid):
        global FLAG
        FLAG = (pageid + 1) % 2
        self.ui.stackedWidget_LR.setCurrentIndex(FLAG)

    #居中显示
    def center(self):
        # 窗口居中
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    #用户(厂商)登录
    def log_in(self, FLAG):
        global USERID
        global MANUFACTURERID
        if FLAG == 0:
            self.ui.success_error_Type.setCurrentIndex(0)
            account_number = self.ui.lineEdit_L_AccountNumber.text()
            password = self.ui.lineEdit_L_Password.text()

            if account_number:
                try:
                    db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
                    cursor = db.cursor()

                    # 直接查询ACCOUNT_NUMBER和PASSWORD两列
                    cursor.execute("SELECT USER_ID, ACCOUNT_NUMBER, PASSWORD FROM user WHERE ACCOUNT_NUMBER = %s",
                                   (account_number,))
                    flag = cursor.fetchone()

                    if not flag:
                        self.ui.success_error_Type.setCurrentIndex(3)  # 没有找到账户
                    else:
                        # 确保查询有结果才尝试访问
                        if flag and flag[2] == password:

                            USERID = str(flag[0])  # 修改全局变量的值
                            self.ui.success_error_Type.setCurrentIndex(1)
                            self.win = MainUserWindow()
                            self.win.show()
                            self.close()
                        else:
                            self.ui.success_error_Type.setCurrentIndex(3)  # 密码错误
                except pymysql.MySQLError as e:
                    print(f"Database Error: {e}")
                    self.ui.success_error_Type.setCurrentIndex(3)  # 数据库错误或其他未知错误
                finally:
                    db.close()

        elif FLAG == 1:
            self.ui.success_error_Type.setCurrentIndex(0)
            account_number = self.ui.lineEdit_L_AccountNumber_manufacture.text()
            password = self.ui.lineEdit_L_Password_manufacturer.text()

            if account_number:
                try:
                    db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
                    cursor = db.cursor()

                    # 直接查询ACCOUNT_NUMBER和PASSWORD两列
                    cursor.execute("SELECT MANUFACTURER_ID, ACCOUNT_NUMBER, PASSWORD FROM manufacturer WHERE ACCOUNT_NUMBER = %s",
                                   (account_number,))
                    flag = cursor.fetchone()

                    if not flag:
                        self.ui.success_error_Type.setCurrentIndex(3)  # 没有找到账户
                    else:
                        # 确保查询有结果才尝试访问
                        if flag and flag[2] == password:
                            MANUFACTURERID = str(flag[0])  # 修改全局变量的值
                            self.ui.success_error_Type.setCurrentIndex(1)
                            self.win = MainManufacturerWindow()
                            self.win.show()
                            self.close()
                        else:
                            self.ui.success_error_Type.setCurrentIndex(3)  # 密码错误
                except pymysql.MySQLError as e:
                    print(f"Database Error: {e}")
                    self.ui.success_error_Type.setCurrentIndex(3)  # 数据库错误或其他未知错误
                finally:
                    db.close()
        else:
            self.ui.success_error_Type.setCurrentIndex(3)  # 账户名长度超过限制

    def register(self, FLAG):
        global USERID
        global MANUFACTURERID
        if FLAG == 0:
            self.ui.success_error_Type.setCurrentIndex(0)

            new_account_number = self.ui.lineEdit_User_R_AccountNumber.text()
            new_password = self.ui.lineEdit_User_R_Password.text()
            new_check_password = self.ui.lineEdit_User_R_CheckPassword.text()

            # 检查用户名和密码长度
            if len(new_account_number) > 10 or len(new_password) > 20 or len(new_account_number) == 0 or len(
                    new_password) == 0:
                self.ui.success_error_Type.setCurrentIndex(4)  # 账户名或密码长度不合适
                return
            elif new_password != new_check_password:
                self.ui.success_error_Type.setCurrentIndex(6)  # 两次密码不一致
                return

            try:
                db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
                cursor = db.cursor()

                # 防止SQL注入，使用参数化查询
                cursor.execute("SELECT * FROM user WHERE ACCOUNT_NUMBER = %s", (new_account_number,))
                flag = cursor.fetchall()

                if not flag:
                    cursor.execute("INSERT INTO user (ACCOUNT_NUMBER, PASSWORD) VALUES (%s, %s)",
                                   (new_account_number, new_password))
                    db.commit()  # 提交事务，确保数据被保存
                    self.ui.success_error_Type.setCurrentIndex(2)  # 显示注册成功
                    # 跳转到用户登录界面 (index 0)
                    QTimer.singleShot(1000, lambda: self.ui.stackedWidget_LR.setCurrentIndex(0))
                else:
                    self.ui.success_error_Type.setCurrentIndex(5)  # 账户已存在
            except pymysql.MySQLError as e:
                print(f"Database Error: {e}")
                self.ui.success_error_Type.setCurrentIndex(3)  # 数据库错误或其他未知错误
            finally:
                db.close()

        elif FLAG == 1:
            self.ui.success_error_Type.setCurrentIndex(0)

            new_account_number = self.ui.lineEdit_Manufacturer_R_AccountNumber.text()
            new_password = self.ui.lineEdit_Manufacturer_R_Password.text()
            new_check_password = self.ui.lineEdit_Manufacturer_R_CheckPassword.text()

            # 检查用户名和密码长度
            if len(new_account_number) > 18 or len(new_password) > 20 or len(new_account_number) == 0 or len(
                    new_password) == 0:
                self.ui.success_error_Type.setCurrentIndex(4)  # 账户名或密码长度不合适
                return
            elif new_password != new_check_password:
                self.ui.success_error_Type.setCurrentIndex(6)  # 两次密码不一致
                return

            try:
                db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
                cursor = db.cursor()

                # 防止SQL注入，使用参数化查询
                cursor.execute("SELECT * FROM manufacturer WHERE ACCOUNT_NUMBER = %s", (new_account_number,))
                flag = cursor.fetchall()

                if not flag:
                    cursor.execute("INSERT INTO manufacturer (ACCOUNT_NUMBER, PASSWORD) VALUES (%s, %s)",
                                   (new_account_number, new_password))
                    db.commit()  # 提交事务，确保数据被保存
                    self.ui.success_error_Type.setCurrentIndex(1)  # 显示注册成功
                    # 跳转到厂商登录界面 (index 1)
                    QTimer.singleShot(1000, lambda: self.ui.stackedWidget_LR.setCurrentIndex(1))
                else:
                    self.ui.success_error_Type.setCurrentIndex(5)  # 账户已存在
            except pymysql.MySQLError as e:
                print(f"Database Error: {e}")
                self.ui.success_error_Type.setCurrentIndex(3)  # 数据库错误或其他未知错误
            finally:
                db.close()


class MainUserWindow(QtWidgets.QMainWindow):
    #是否推荐
    new_game_score = 1  # 1表示好评，0表示差评，默认好评
    evaluation_frames = []  # 初始化评价帧列表
    def __init__(self):
        super().__init__()
        self.ui = Ui_testwindow()  # 注意这里是实例化对象
        self.ui.setupUi(self)
        self.ui.stackedWidget_Window.setCurrentIndex(0)

        # 设置窗口无边框及透明背景
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 窗口居中
        self.center()

        # 添加退出按钮
        exit_button = QPushButton(self)
        exit_button.setText("X")
        exit_button.setGeometry(QtCore.QRect(self.width() - 50, 10, 40, 40))
        exit_button.setStyleSheet("""
                   QPushButton {
                       background-color: rgba(255, 255, 255, 50);
                       color: white;
                       font: 14pt "微软雅黑";
                       border-radius: 5px;
                   }
                   QPushButton:hover {
                       background-color: rgba(255, 0, 0, 100);
                   }
               """)
        exit_button.clicked.connect(self.close)
        #按钮绑定
        #搜索按钮绑定
        self.ui.pushButton_SearchGame.clicked.connect(self.show_searchgame_page)
        # self.ui.pushButton_SearchGame.clicked.connect(self.on_pushButton_SearchGame_clicked)
        # 添加 Enter 键触发搜索
        self.ui.lineEdit_SearchGame.returnPressed.connect(self.show_searchgame_page)
        #跳转商城主页按钮绑定
        self.ui.pushButton_GoMainPage.clicked.connect(self.show_allgames_page)
        #跳转好友界面按钮绑定
        self.ui.pushButton_GoFriendPage.clicked.connect(self.show_personal_friends_page)
        #跳转库界面按钮绑定
        self.ui.pushButton_GoGameLibraryPage.clicked.connect(self.show_personal_gamelibrary_page)
        #跳转购物车界面按钮绑定
        self.ui.pushButton_GoShoppingCartPage.clicked.connect(self.show_personal_shoppingcart_page)

        #设置窗口布局
        self.scrollAreaLayout = QVBoxLayout(self.ui.scrollAreaWidgetContents_3)
        self.ui.scrollAreaWidgetContents_3.setLayout(self.scrollAreaLayout)

        #连接数据库
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
        cursor = db.cursor()

        # 防止SQL注入，使用参数化查询
        print(f"{USERID}")
        cursor.execute(f"SELECT ACCOUNT_NUMBER FROM user WHERE USER_ID = %s", {USERID})
        user_name = cursor.fetchone()

        # 关闭数据库连接
        db.close()

        if user_name:
            self.ui.pushButton_GoPersonalPage.setText(user_name[0])
        else:
            print("No user found with the given ID")

        self.show_allgames_page()

        self.show()

    def show_allgames_page(self):
        self.ui.stackedWidget_Window.setCurrentIndex(0)
        # 连接数据库
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
        cursor = db.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM game")
        game_count = int(cursor.fetchone()[0])

        # 查询所有游戏具体信息
        cursor.execute("SELECT GAME_NAME, introduction, price FROM game")

        # 获取所有游戏具体信息
        all_game = cursor.fetchall()
        for i in range(0, game_count):
            print(f"{all_game[i][0]},{all_game[i][1]},{all_game[i][2]}")
        # 关闭数据库连接
        db.close()

        all_game = list(all_game)
        x = 207  # 初始化x坐标
        y = 180  # 初始化y坐标

        for i in range(0, game_count):
            self.add_page(x, y, all_game[i][0], all_game[i][1], all_game[i][2])
            # self.add_page(x, y, test_game[i][0], test_game[i][1], test_game[i][2])
            y += 160
            self.update()

        self.show()

    #居中显示
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

     # 将游戏块添加到页面上
    def add_page(self, x, y, name, introduction, cost):
        frame = QFrame(parent=self.ui.scrollAreaWidgetContents)  # 显式指定父对象为scroll
        frame.move(x, y)
        frame.setMinimumSize(615, 150)
        frame.setMaximumSize(615, 150)
        frame.setStyleSheet("background-color: rgb(59, 59, 89);")
        frame.setObjectName("Frame")

        layoutWidget = QtWidgets.QWidget(frame)
        layoutWidget.setGeometry(QtCore.QRect(0, 0, 615, 150))
        layoutWidget.setObjectName("layoutWidget")

        game_frame = QtWidgets.QVBoxLayout(layoutWidget)
        game_frame.setContentsMargins(3, 3, 3, 3)
        game_frame.setObjectName("Frame_Game")

        # 游戏名称栏 - 改为可点击的QPushButton
        Game_Name = QtWidgets.QPushButton(layoutWidget)
        Game_Name.setMouseTracking(True)
        Game_Name.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 255, 255,20);
                font: 15pt "微软雅黑";
                color: rgb(255, 255, 255);
                text-align: left;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                color: rgb(200, 200, 255);
                text-decoration: underline;
            }
        """)
        Game_Name.setText(f"{name}")
        Game_Name.setObjectName("Game_Name")
        Game_Name.clicked.connect(lambda: self.evaluate_game_page(name))  # 点击跳转到评价界面
        game_frame.addWidget(Game_Name)

        # 游戏简介栏
        Game_Introduction = QtWidgets.QPlainTextEdit(layoutWidget)
        Game_Introduction.setReadOnly(True)  # 设置为只读模式
        Game_Introduction.setMouseTracking(True)
        Game_Introduction.setStyleSheet("""
            background-color: rgb(255, 255, 255,20);
            font: 10pt "微软雅黑";
            color: rgb(255, 255, 255);
            border:none;
        """)
        Game_Introduction.setLineWidth(-1)
        Game_Introduction.setPlainText(f"{introduction}")
        Game_Introduction.setObjectName("Game_I")
        game_frame.addWidget(Game_Introduction)

        # 功能栏
        horizontalLayout_2 = QtWidgets.QHBoxLayout()
        horizontalLayout_2.setObjectName("horizontalLayout_2")

        pushButton_2 = QtWidgets.QPushButton(layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pushButton_2.sizePolicy().hasHeightForWidth())
        pushButton_2.setSizePolicy(sizePolicy)
        pushButton_2.setStyleSheet("""
            QPushButton {
                color: rgb(229, 255, 255);
                background-color: rgba(255, 255, 255, 50); 
            }
        """)
        pushButton_2.setText("")
        pushButton_2.setObjectName("pushButton_2")
        horizontalLayout_2.addWidget(pushButton_2)

        pushButton_3 = QtWidgets.QPushButton(layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pushButton_3.sizePolicy().hasHeightForWidth())
        pushButton_3.setSizePolicy(sizePolicy)
        pushButton_3.setStyleSheet("""
            QPushButton {
                color: rgb(229, 255, 255);
                background-color: rgba(255, 255, 255, 50); 
            }
        """)
        pushButton_3.setText("")
        pushButton_3.setObjectName("pushButton_3")
        horizontalLayout_2.addWidget(pushButton_3)

        pushButton_4 = QtWidgets.QPushButton(layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pushButton_4.sizePolicy().hasHeightForWidth())
        pushButton_4.setSizePolicy(sizePolicy)
        pushButton_4.setStyleSheet("""
            QPushButton {
                color: rgb(229, 255, 255);
                background-color: rgba(255, 255, 255, 50); 
            }
        """)
        pushButton_4.setText("")
        pushButton_4.setObjectName("pushButton_4")
        horizontalLayout_2.addWidget(pushButton_4)

        label_6 = QtWidgets.QLabel(layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(label_6.sizePolicy().hasHeightForWidth())
        label_6.setSizePolicy(sizePolicy)
        label_6.setStyleSheet("""
            font: 9pt "黑体";
            color:rgb(255, 255, 255);
        """)
        label_6.setText(f"{cost}")
        label_6.setWordWrap(False)
        label_6.setObjectName("label_6")
        horizontalLayout_2.addWidget(label_6)

        # 添加购物车控件
        pushButton = QtWidgets.QPushButton(layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pushButton.sizePolicy().hasHeightForWidth())
        pushButton.setSizePolicy(sizePolicy)
        pushButton.setStyleSheet("""
            QPushButton {
                background-color: rgb(92, 138, 0);
                color: rgb(255, 255, 255);
            }
        """)
        pushButton.setText("加入购物车")
        pushButton.setObjectName("pushButton")
        pushButton.clicked.connect(lambda: self.add_game_to_shoppingcart(name, USERID))
        horizontalLayout_2.addWidget(pushButton)

        game_frame.addLayout(horizontalLayout_2)

    #添加游戏到购物车
    def add_game_to_shoppingcart(self, game_name, USERID):
        """
        尝试将指定游戏添加到用户的购物车中。
        首先检查游戏是否已在用户的游戏库中（having_games表），
        然后检查该游戏是否已存在于购物车（通过order_for_goods及order_details表联合检查）中。
        如果游戏不在上述任一位置，则将其插入购物车，并标记状态为未购买。
        """
        with pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system') as db, \
                db.cursor() as cursor:

            # 检查游戏是否已在用户的游戏库中
            cursor.execute("SELECT GAME_ID FROM having_games WHERE USER_ID = %s", (USERID,))
            all_having_games_ids = [id[0] for id in cursor.fetchall()]

            # 获取游戏ID
            cursor.execute("SELECT GAME_ID FROM game WHERE GAME_NAME = %s", (game_name,))
            game_id = cursor.fetchone()

            # 如果游戏已在用户游戏库中，则不进行添加操作
            if game_id and game_id[0] in all_having_games_ids:
                print("此游戏已在用户游戏库中，无法添加至购物车。")
                return

            # 检查用户是否有未完成的订单
            cursor.execute("SELECT ORDER_ID FROM order_for_goods WHERE USER_ID = %s AND ORDER_STATE = 0", (USERID,))
            order_id = cursor.fetchone()

            # 如果有未完成订单
            if order_id:
                # 首先检查游戏是否已经在该订单的购物车中
                cursor.execute("SELECT 1 FROM order_details WHERE ORDER_ID = %s AND GAME_ID = %s",
                               (order_id[0], game_id[0]))
                game_already_in_cart = cursor.fetchone()

                # 如果游戏尚未添加，则插入
                if not game_already_in_cart:
                    now_date = datetime.datetime.now() # 获取当前日期
                    cursor.execute(
                        "INSERT INTO order_details (ORDER_ID, GAME_ID, DETAIL_TIME, BUY_OR_REFUND) VALUES (%s, %s, %s, 0)",
                        (order_id[0], game_id[0], now_date))
                    db.commit()
                    print(f"游戏'{game_name}'已成功添加至购物车1。")
                    return
                else:
                    print(f"游戏'{game_name}'已存在于订单{order_id[0]}的购物车中。")
                    return

            # 如果没有未完成订单，创建新订单并添加游戏
            else:
                now_date = datetime.datetime.now()
                cursor.execute("INSERT INTO order_for_goods (USER_ID, ORDER_STATE, ORDER_TIME) VALUES (%s, 0, %s)",
                               (USERID, now_date))
                cursor.execute(
                    "SELECT ORDER_ID FROM order_for_goods WHERE USER_ID = %s AND ORDER_STATE = 0 ORDER BY ORDER_ID DESC LIMIT 1",
                    (USERID,))
                new_order_id = cursor.fetchone()[0]
                cursor.execute(
                    "INSERT INTO order_details (ORDER_ID, GAME_ID, DETAIL_TIME, BUY_OR_REFUND) VALUES (%s, %s, %s, 0)",
                    (new_order_id, game_id[0], now_date))
                db.commit()
                print(f"游戏'{game_name}'已成功添加至新创建的订单中。")

        print(f"游戏'{game_name}'已成功添加至购物车2。")
        self.show()

    def show_searchgame_page(self):
        self.ui.stackedWidget_Window.setCurrentIndex(1)

        # 清除旧控件
        for widget in self.ui.scrollAreaWidgetContents_3.findChildren(QWidget):
            widget.deleteLater()
        QApplication.processEvents()  # 确保删除操作完成

        # 连接数据库
        with pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system') as db:
            cursor = db.cursor()

            keyword = self.ui.lineEdit_SearchGame.text()

            # 查询游戏数量
            cursor.execute("SELECT COUNT(*) FROM game WHERE GAME_NAME LIKE %s", ('%' + keyword + '%',))
            game_count = int(cursor.fetchone()[0])

            # 查询所有游戏具体信息
            cursor.execute("SELECT GAME_NAME, introduction, price FROM game WHERE GAME_NAME LIKE %s",
                           ('%' + keyword + '%',))
            all_game = cursor.fetchall()

            # 打印游戏信息（用于调试，可在生产环境中移除）
            for game in all_game:
                print(f"{game[0]},{game[1]},{game[2]}")

            nx = 207
            ny = 180

            for game in all_game:
                self.add_searched_page(nx, ny, game[0], game[1], game[2])
                ny += 160

        # 移除多余的 update() 调用
        self.show()

    #将关键字查找结果添加到页面上
    def add_searched_page(self, x, y, name, introduction, cost):
        frame = QFrame(parent=self.ui.scrollAreaWidgetContents_3)  # 显式指定父对象为scroll
        frame.move(x, y)
        frame.setMinimumSize(615, 150)
        frame.setMaximumSize(615, 150)
        frame.setStyleSheet("background-color: rgb(59, 59, 89);")
        frame.setObjectName("Frame")

        layoutWidget = QtWidgets.QWidget(frame)
        layoutWidget.setGeometry(QtCore.QRect(0, 0, 615, 150))
        layoutWidget.setObjectName("layoutWidget")

        game_frame = QtWidgets.QVBoxLayout(layoutWidget)
        game_frame.setContentsMargins(3, 3, 3, 3)
        game_frame.setObjectName("Frame_Game")

        # 游戏名称栏 - 改为可点击的QPushButton
        Game_Name = QtWidgets.QPushButton(layoutWidget)
        Game_Name.setMouseTracking(True)
        Game_Name.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 255, 255,20);
                font: 15pt "微软雅黑";
                color: rgb(255, 255, 255);
                text-align: left;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                color: rgb(200, 200, 255);
                text-decoration: underline;
            }
        """)
        Game_Name.setText(f"{name}")
        Game_Name.setObjectName("Game_Name")
        Game_Name.clicked.connect(lambda: self.evaluate_game_page(name))  # 点击跳转到评价界面
        game_frame.addWidget(Game_Name)

        # 游戏简介栏
        Game_Introduction = QtWidgets.QPlainTextEdit(layoutWidget)
        Game_Introduction.setReadOnly(True)  # 设置为只读模式
        Game_Introduction.setMouseTracking(True)
        Game_Introduction.setStyleSheet("""
            background-color: rgb(255, 255, 255,20);
            font: 10pt "微软雅黑";
            color: rgb(255, 255, 255);
            border:none;
        """)
        Game_Introduction.setLineWidth(-1)
        Game_Introduction.setPlainText(f"{introduction}")
        Game_Introduction.setObjectName("Game_I")
        game_frame.addWidget(Game_Introduction)

        # 功能栏
        horizontalLayout_2 = QtWidgets.QHBoxLayout()
        horizontalLayout_2.setObjectName("horizontalLayout_2")

        pushButton_2 = QtWidgets.QPushButton(layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pushButton_2.sizePolicy().hasHeightForWidth())
        pushButton_2.setSizePolicy(sizePolicy)
        pushButton_2.setStyleSheet("""
            QPushButton {
                color: rgb(229, 255, 255);
                background-color: rgba(255, 255, 255, 50); 
            }
        """)
        pushButton_2.setText("")
        pushButton_2.setObjectName("pushButton_2")
        horizontalLayout_2.addWidget(pushButton_2)

        pushButton_3 = QtWidgets.QPushButton(layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pushButton_3.sizePolicy().hasHeightForWidth())
        pushButton_3.setSizePolicy(sizePolicy)
        pushButton_3.setStyleSheet("""
            QPushButton {
                color: rgb(229, 255, 255);
                background-color: rgba(255, 255, 255, 50); 
            }
        """)
        pushButton_3.setText("")
        pushButton_3.setObjectName("pushButton_3")
        horizontalLayout_2.addWidget(pushButton_3)

        pushButton_4 = QtWidgets.QPushButton(layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pushButton_4.sizePolicy().hasHeightForWidth())
        pushButton_4.setSizePolicy(sizePolicy)
        pushButton_4.setStyleSheet("""
            QPushButton {
                color: rgb(229, 255, 255);
                background-color: rgba(255, 255, 255, 50); 
            }
        """)
        pushButton_4.setText("")
        pushButton_4.setObjectName("pushButton_4")
        horizontalLayout_2.addWidget(pushButton_4)

        label_6 = QtWidgets.QLabel(layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(label_6.sizePolicy().hasHeightForWidth())
        label_6.setSizePolicy(sizePolicy)
        label_6.setStyleSheet("""
            font: 9pt "黑体";
            color:rgb(255, 255, 255);
        """)
        label_6.setText(f"{cost}")
        label_6.setWordWrap(False)
        label_6.setObjectName("label_6")
        horizontalLayout_2.addWidget(label_6)

        # 添加购物车控件
        pushButton = QtWidgets.QPushButton(layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pushButton.sizePolicy().hasHeightForWidth())
        pushButton.setSizePolicy(sizePolicy)
        pushButton.setStyleSheet("""
            QPushButton {
                background-color: rgb(92, 138, 0);
                color: rgb(255, 255, 255);
            }
        """)
        pushButton.setText("加入购物车")
        pushButton.setObjectName("pushButton")
        pushButton.clicked.connect(lambda: self.add_game_to_shoppingcart(name, USERID))
        horizontalLayout_2.addWidget(pushButton)

        game_frame.addLayout(horizontalLayout_2)
        frame.show()

    #显示个人好友界面
    def show_personal_friends_page(self):
        self.ui.stackedWidget_Window.setCurrentIndex(2)
        self.ui.stackedWidget_userFriendPage.setCurrentIndex(0)

        #绑定跳转显示好友界面
        self.ui.pushButton_ShowUserFriends.clicked.connect(self.show_personal_friends_page)

        #绑定跳转添加好友界面的按钮
        self.ui.pushButton_ShowAddFriend.clicked.connect(lambda: self.ui.stackedWidget_userFriendPage.setCurrentIndex(1))
        self.ui.pushButton_search.clicked.connect(self.show_addfriend_page)

        #绑定查看好友申请界面的按钮
        self.ui.pushButton_ShowApplication.clicked.connect(self.show_application_page)
        # 连接数据库
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
        cursor = db.cursor()

        # 防止SQL注入，使用参数化查询
        print(f"{USERID}")

        #查询当前用户姓名
        cursor.execute(f"SELECT ACCOUNT_NUMBER FROM user WHERE USER_ID = '{USERID}';")
        user_name = cursor.fetchone()

        #查询当前用户好友数量
        cursor.execute(f"SELECT COUNT(*) FROM friend Where USER_ID = '{USERID}';")
        firend_count = int(cursor.fetchone()[0])

        print(f"{firend_count}")

        #查询好友用户名
        cursor.execute(f"SELECT u.ACCOUNT_NUMBER FROM friend f JOIN user u ON f.FRIEND_ID = u.USER_ID WHERE f.USER_ID = %s AND f.STATE = 1;",(USERID))
        all_friend = list(cursor.fetchall())

        # 关闭数据库连接
        db.close()

        x = 17
        y = 10

        if all_friend:
            for i in range(0, firend_count):
                print(f"{all_friend[i][0]}")
                self.add_user_friends(x, y, all_friend[i][0])
                x += 267
        else:
            print(f"用户{user_name[0]}暂时没有好友")
        self.ui.label_Show_UserName.setText(f"{user_name[0]}")

    #添加好友链接块
    def add_user_friends(self, x, y, name):
        frame_Friend = QFrame(parent=self.ui.scrollAreaWidgetContents_2)
        frame_Friend.move(x, y)
        frame_Friend.setMinimumSize(250, 80)
        frame_Friend.setMaximumSize(250, 80)
        frame_Friend.setStyleSheet("background-color: rgb(128, 134, 255);")
        frame_Friend.setObjectName('frame_' + name)

        pushButton_Friend = QtWidgets.QPushButton(frame_Friend)
        pushButton_Friend.setGeometry(QtCore.QRect(10, 10, 60, 60))
        pushButton_Friend.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/u=772358879,2131786806&fm=253&fmt=auto&app=138&f=JPEG.webp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        pushButton_Friend.setIcon(icon)
        pushButton_Friend.setIconSize(QtCore.QSize(60, 60))
        pushButton_Friend.setObjectName("pushButton_Friend")
        pushButton_Friend.clicked.connect(lambda: self.show_friend_page(name))

        label_FriendName = QtWidgets.QLabel(frame_Friend)
        label_FriendName.setGeometry(QtCore.QRect(90, 30, 141, 21))
        label_FriendName.setText(f"{name}")
        label_FriendName.setObjectName("label_FriendName")

        frame_Friend.show()

    #显示好友主页
    def show_friend_page(self, friend_name):
        self.ui.stackedWidget_Window.setCurrentIndex(3)

        self.ui.label_Show_FriendName.setText(f"{friend_name}")

    #添加好友的界面
    def show_addfriend_page(self):
        # 连接数据库对目标用户进行检查
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
        cursor = db.cursor()

        new_searched_friendname = self.ui.lineEdit_addSearchName.text()
        cursor.execute("SELECT USER_ID FROM user WHERE ACCOUNT_NUMBER = %s", (new_searched_friendname,))
        new_friend_id = cursor.fetchone()

        if new_friend_id:
            # 检查是否已存在好友申请
            cursor.execute(
                "SELECT COUNT(*) FROM friend WHERE FRIEND_ID = %s AND USER_ID = %s AND STATE = 0",
                (new_friend_id[0], USERID))
            flag = cursor.fetchone()[0]

            if not flag:
                # 如果没有好友关系，准备显示添加好友界面
                x = 100
                y = 50
                self.add_searched_friend_page(x, y, new_searched_friendname)
                y += 230
                self.show()
            else:
                # 已经是好友，给用户一个反馈
                print("提示, 目标用户已与您建立好友关系。")
        else:
            # 用户不存在，给用户一个反馈
            print("提示, 找不到指定的目标用户。")

    #显示查询到的好友信息到添加好友界面
    def add_searched_friend_page(self, x, y, friend_name):
        frame_Friend = QFrame(parent=self.ui.frame_showSearchedPage)
        frame_Friend.move(x, y)
        frame_Friend.setMinimumSize(440, 200)
        frame_Friend.setMaximumSize(440, 200)
        frame_Friend.setStyleSheet("background-color: rgb(128, 134, 255);")
        frame_Friend.setObjectName('frame_' + friend_name)

        pushButton_Friend = QtWidgets.QPushButton(frame_Friend)
        pushButton_Friend.setGeometry(QtCore.QRect(310, 50, 100, 100))
        pushButton_Friend.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/u=772358879,2131786806&fm=253&fmt=auto&app=138&f=JPEG.webp"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        pushButton_Friend.setIcon(icon)
        pushButton_Friend.setIconSize(QtCore.QSize(100, 100))
        pushButton_Friend.setObjectName("pushButton_Friend")

        # 修改这里：使用lambda捕获friend_name，并添加错误处理
        pushButton_Friend.clicked.connect(lambda checked, name=friend_name: self.safe_add_friend_request(name))

        label_FriendName = QtWidgets.QLabel(frame_Friend)
        label_FriendName.setGeometry(QtCore.QRect(30, 50, 300, 100))
        label_FriendName.setText(f"{friend_name}")
        label_FriendName.setObjectName("label_FriendName")

        frame_Friend.show()

    def safe_add_friend_request(self, friend_name):
        try:
            print(f"尝试添加好友: {friend_name}")  # 调试信息
            self.add_user_friendrequest(friend_name)
        except Exception as e:
            print(f"添加好友请求时出错: {e}")
            import traceback
            traceback.print_exc()

    #添加好友方法实现
    # def add_user_friendrequest(self, new_friend_name):
    #     try:
    #         # 连接数据库
    #         db = pymysql.connect(host="localhost", user="root", password='123456',
    #                              port=3306, db='game_system')
    #         cursor = db.cursor()
    #
    #         # 1. 查询目标用户ID
    #         cursor.execute("SELECT USER_ID FROM user WHERE ACCOUNT_NUMBER = %s",
    #                        (new_friend_name,))
    #         new_friend_id = cursor.fetchone()
    #
    #         if not new_friend_id:
    #             print(f"用户 {new_friend_name} 不存在")
    #             return
    #
    #         new_friend_id = new_friend_id[0]  # 获取实际ID值
    #
    #         # 2. 检查是否已经是好友或已有申请
    #         cursor.execute("""
    #             SELECT STATE FROM friend
    #             WHERE USER_ID = %s AND FRIEND_ID = %s
    #         """, (USERID, new_friend_id))
    #
    #         existing_relation = cursor.fetchone()
    #
    #         if existing_relation:
    #             if existing_relation[0] == 1:
    #                 print("你们已经是好友了")
    #             elif existing_relation[0] == 0:
    #                 print("已发送过好友申请，等待对方处理")
    #             return
    #
    #         # 3. 插入好友申请
    #         cursor.execute("""
    #             INSERT INTO friend (USER_ID, FRIEND_ID, STATE)
    #             VALUES (%s, %s, 0)
    #         """, (USERID, new_friend_id))
    #
    #         db.commit()
    #         print(f"已向 {new_friend_name} 发送好友申请")
    #
    #     except pymysql.MySQLError as e:
    #         print(f"数据库错误: {e}")
    #         if 'db' in locals():
    #             db.rollback()
    #     except Exception as e:
    #         print(f"其他错误: {e}")
    #     finally:
    #         if 'cursor' in locals():
    #             cursor.close()
    #         if 'db' in locals():
    #             db.close()
    def add_user_friendrequest(self, new_friend_name):
        try:
            # 连接数据库
            db = pymysql.connect(host="localhost", user="root", password='123456',
                                 port=3306, db='game_system')
            cursor = db.cursor()

            # 1. 查询目标用户ID
            cursor.execute("SELECT USER_ID FROM user WHERE ACCOUNT_NUMBER = %s",
                           (new_friend_name,))
            new_friend_id = cursor.fetchone()

            if not new_friend_id:
                QMessageBox.warning(self, "提示", f"用户 {new_friend_name} 不存在")
                return

            new_friend_id = new_friend_id[0]  # 获取实际ID值

            # 2. 检查是否已经是好友或已有申请
            cursor.execute("""
                SELECT STATE FROM friend 
                WHERE USER_ID = %s AND FRIEND_ID = %s
            """, (USERID, new_friend_id))

            existing_relation = cursor.fetchone()

            if existing_relation:
                if existing_relation[0] == 1:
                    QMessageBox.information(self, "提示", "你们已经是好友了")
                elif existing_relation[0] == 0:
                    QMessageBox.information(self, "提示", "好友申请已存在")
                return

            # 3. 插入好友申请
            cursor.execute("""
                INSERT INTO friend (USER_ID, FRIEND_ID, STATE)
                VALUES (%s, %s, 0)
            """, (USERID, new_friend_id))

            db.commit()
            QMessageBox.information(self, "提示", f"已向 {new_friend_name} 发送好友申请")

        except pymysql.MySQLError as e:
            QMessageBox.critical(self, "错误", f"数据库错误: {e}")
            if 'db' in locals():
                db.rollback()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"其他错误: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'db' in locals():
                db.close()

    def show_friend_games(self, friend_name):
        # 清除旧控件
        for widget in self.ui.scrollAreaWidgetContents_GameLibrary.findChildren(QWidget):
            widget.deleteLater()
        QApplication.processEvents()  # 确保删除操作完成

        # 连接数据库
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
        cursor = db.cursor()

        try:
            # 获取好友ID
            cursor.execute("SELECT USER_ID FROM user WHERE ACCOUNT_NUMBER = %s", (friend_name,))
            friend_id = cursor.fetchone()
            if not friend_id:
                print(f"找不到用户: {friend_name}")
                return

            # 查询好友拥有的游戏
            cursor.execute("""
                SELECT g.GAME_NAME 
                FROM having_games hg
                JOIN game g ON hg.GAME_ID = g.GAME_ID
                WHERE hg.USER_ID = %s
            """, (friend_id[0],))
            friend_games = cursor.fetchall()

            # 显示好友游戏
            x = 20
            y = 20
            for game in friend_games:
                self.add_friend_game(x, y, game[0])
                y += 90

            # 更新界面显示
            self.ui.stackedWidget_Window.setCurrentIndex(4)  # 切换到游戏库页面
            self.ui.label_Show_UserName_2.setText(f"{friend_name}的游戏库")  # 更新标题

        except Exception as e:
            print(f"查询好友游戏时出错: {e}")
        finally:
            cursor.close()
            db.close()

    def add_friend_game(self, x, y, game_name):
        frame_gamelibrary = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents_GameLibrary)
        frame_gamelibrary.move(x, y)
        frame_gamelibrary.setMinimumSize(506, 70)
        frame_gamelibrary.setMaximumSize(506, 70)
        frame_gamelibrary.setStyleSheet("background-color: rgb(59, 59, 89);")
        frame_gamelibrary.setObjectName("frame")

        Game_Name = QtWidgets.QLabel(frame_gamelibrary)
        Game_Name.setGeometry(QtCore.QRect(3, 3, 500, 26))
        Game_Name.setMouseTracking(True)
        Game_Name.setStyleSheet("""
            QWidget {
                background-color: rgb(255, 255, 255,20);
                font: 15pt "微软雅黑";
                color: rgb(255, 255, 255);
            }
        """)
        Game_Name.setText(f"{game_name}")
        Game_Name.setObjectName("Game_Name")

        # 这里可以添加其他元素，如游戏图片等
        frame_gamelibrary.show()

    #显示其他用户对当前用户的好友申请
    def show_application_page(self):
        self.ui.stackedWidget_userFriendPage.setCurrentIndex(2)
        # 连接数据库
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
        cursor = db.cursor()

        # 防止SQL注入，使用参数化查询
        print(f"{USERID}")

        #查询对当前用户发出好友申请的用户id
        cursor.execute(f"SELECT u.ACCOUNT_NUMBER FROM friend f join user u ON f.USER_ID = u.USER_ID WHERE FRIEND_ID = %s AND STATE = 0",
                       (USERID,))
        user_names = cursor.fetchall()

        cursor.close()
        db.close()

        x = 40
        y = 20
        for user in user_names:
            print(f"{user[0]}")
            self.add_application_user(x, y, user[0])
            y += 80
        self.show()

    #添加好友请求信息到页面上
    def add_application_user(self, x, y, username):
        frame_applicationuser = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents_applicationUser)
        frame_applicationuser.move(x, y)
        frame_applicationuser.setMinimumSize(700, 70)
        frame_applicationuser.setMaximumSize(700, 70)
        frame_applicationuser.setStyleSheet("background-color: rgb(59, 59, 89);  ")
        frame_applicationuser.setObjectName("frame")

        User_Name = QtWidgets.QLabel(frame_applicationuser)
        User_Name.setGeometry(QtCore.QRect(3, 3, 700, 30))
        User_Name.setMouseTracking(True)
        User_Name.setStyleSheet("QWidget {\n"
                                "    background-color: rgb(255, 255, 255,20);\n"
                                "    font: 15pt \"微软雅黑\";\n"
                                "    color: rgb(255, 255, 255);\n"
                                "     }\n"
                                "")
        User_Name.setText(f"{username}")
        User_Name.setObjectName("User_Name")

        pushButton_Agree = QtWidgets.QPushButton(frame_applicationuser)
        pushButton_Agree.setGeometry(QtCore.QRect(530, 40, 75, 20))
        pushButton_Agree.setStyleSheet("QPushButton {\n"
                                          "         background-color: rgb(92, 138, 0);\n"
                                          "    color: rgb(255, 255, 255);\n"
                                          "     }")
        pushButton_Agree.setObjectName("pushButton_Agree")
        pushButton_Agree.clicked.connect(lambda: self.agree_friend(username))
        pushButton_Agree.setText("通过")

        pushButton_Reject = QtWidgets.QPushButton(frame_applicationuser)
        pushButton_Reject.setGeometry(QtCore.QRect(625, 40, 75, 20))
        pushButton_Reject.setStyleSheet("QPushButton {\n"
                                           "         background-color: rgb(154, 231, 231);\n"
                                           "    color: rgb(255, 255, 255);\n"
                                           "     }")
        pushButton_Reject.setObjectName("pushButton_Reject")
        pushButton_Reject.clicked.connect(lambda: self.disagree_friend(username))
        pushButton_Reject.setText("拒绝")

        frame_applicationuser.show()

    #通过好友申请
    def agree_friend(self, friendname):
        # 连接数据库
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
        cursor = db.cursor()
        #查询目标好友id
        cursor.execute("SELECT USER_ID FROM user WHERE ACCOUNT_NUMBER = %s",
                       (friendname,))
        friend_id = cursor.fetchone()[0]

        #修改好友表中的状态，并且新增双向状态
        cursor.execute("UPDATE friend SET STATE = 1 WHERE FRIEND_ID = %s AND USER_ID = %s",
                       (USERID, friend_id))
        cursor.execute("INSERT INTO friend (FRIEND_ID, USER_ID, STATE) VALUES (%s, %s, 1)",
            (friend_id, USERID))
        db.commit()
        db.close()

        self.reload_application()

    #拒绝好友申请
    def disagree_friend(self, friendname):
        # 连接数据库
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
        cursor = db.cursor()
        # 查询目标好友id
        cursor.execute("SELECT USER_ID FROM user WHERE ACCOUNT_NUMBER = %s",
                       (friendname,))
        friend_id = cursor.fetchone()[0]

        #修改好友表中的状态，删除关系
        cursor.execute("DELETE FROM friend WHERE FRIEND_ID = %s AND USER_ID = %s AND STATE = 0",
                       (USERID, friend_id))
        db.commit()
        db.close()

        self.reload_application()

    #重新加载页面
    def reload_application(self):
        # 获取scrollAreaWidgetContents_Shoppingcart中的所有子部件
        children_widgets = self.ui.scrollAreaWidgetContents_applicationUser.findChildren(QWidget)
        # self.ui.emptyCartLable.setVisible(False)

        # 遍历并删除所有子部件，但跳过名为'emptyCartLabel'的控件
        for child in children_widgets:
            child.deleteLater()

        # 确保所有删除操作完成
        QApplication.processEvents()

        self.ui.stackedWidget_userFriendPage.setCurrentIndex(2)
        # 连接数据库
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
        cursor = db.cursor()

        # 防止SQL注入，使用参数化查询
        print(f"{USERID}")

        # 查询对当前用户发出好友申请的用户id
        cursor.execute(
            f"SELECT u.ACCOUNT_NUMBER FROM friend f join user u ON f.USER_ID = u.USER_ID WHERE FRIEND_ID = %s AND STATE = 0",
            (USERID,))
        user_names = cursor.fetchall()

        cursor.close()
        db.close()

        x = 40
        y = 20
        for user in user_names:
            print(f"{user[0]}")
            self.add_application_user(x, y, user[0])

    #显示用户游戏库页面
    def show_personal_gamelibrary_page(self):
        try:
            self.ui.stackedWidget_Window.setCurrentIndex(4)

            # 清除旧控件
            self.ui.listWidget_3.clear()

            # 连接数据库
            with pymysql.connect(host="localhost", user="root", password='123456',
                                 port=3306, db='game_system') as db:
                cursor = db.cursor()

                # 1. 首先添加"全部"按钮
                all_item = QtWidgets.QListWidgetItem("全部")
                all_item.setData(QtCore.Qt.UserRole, "all")
                self.ui.listWidget_3.addItem(all_item)

                # 2. 查询用户拥有的游戏种类（从GAME_TO_TYPE表获取）
                cursor.execute("""
                    SELECT DISTINCT gt.TYPE_NAME 
                    FROM having_games hg
                    JOIN GAME_TO_TYPE gt ON hg.GAME_ID = gt.GAME_ID
                    WHERE hg.USER_ID = %s
                """, (USERID,))
                game_types = cursor.fetchall()

                # 3. 添加游戏种类到列表
                for game_type in game_types:
                    item = QtWidgets.QListWidgetItem(game_type[0])
                    item.setData(QtCore.Qt.UserRole, game_type[0])
                    self.ui.listWidget_3.addItem(item)

                # 断开之前的连接，避免重复连接
                try:
                    self.ui.listWidget_3.itemClicked.disconnect()
                except:
                    pass

                # 4. 连接点击事件
                self.ui.listWidget_3.itemClicked.connect(self.filter_games_by_type)

                # 初始加载所有游戏
                self.filter_games_by_type(all_item)

        except Exception as e:
            print(f"Error in show_personal_gamelibrary_page: {e}")
            import traceback
            traceback.print_exc()

    def filter_games_by_type(self, item):
        try:
            selected_type = item.data(QtCore.Qt.UserRole)

            # 清除旧游戏列表
            for widget in self.ui.scrollAreaWidgetContents_GameLibrary.findChildren(QtWidgets.QWidget):
                widget.deleteLater()
            QApplication.processEvents()  # 确保删除完成

            # 连接数据库
            with pymysql.connect(host="localhost", user="root", password='123456',
                                 port=3306, db='game_system') as db:
                cursor = db.cursor()

                if selected_type == "all":
                    cursor.execute("""
                        SELECT g.GAME_NAME 
                        FROM having_games hg
                        JOIN game g ON hg.GAME_ID = g.GAME_ID
                        WHERE hg.USER_ID = %s
                    """, (USERID,))
                else:
                    cursor.execute("""
                        SELECT g.GAME_NAME 
                        FROM having_games hg
                        JOIN game g ON hg.GAME_ID = g.GAME_ID
                        JOIN GAME_TO_TYPE gt ON g.GAME_ID = gt.GAME_ID
                        WHERE hg.USER_ID = %s AND gt.TYPE_NAME = %s
                    """, (USERID, selected_type))

                games = cursor.fetchall()

                x = 20
                y = 20

                for game in games:
                    self.add_gamelibrary_page(x, y, game[0])
                    y += 90

        except Exception as e:
            print(f"Error in filter_games_by_type: {e}")
            import traceback
            traceback.print_exc()
    #添加用户游戏到页面上
    def add_gamelibrary_page(self, x, y, game_name):
        frame_gamelibrary = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents_GameLibrary)
        frame_gamelibrary.move(x, y)
        frame_gamelibrary.setMinimumSize(506, 70)
        frame_gamelibrary.setMaximumSize(506, 70)
        frame_gamelibrary.setStyleSheet("background-color: rgb(59, 59, 89);  ")
        frame_gamelibrary.setObjectName("frame")

        Game_Name = QtWidgets.QLabel(frame_gamelibrary)
        Game_Name.setGeometry(QtCore.QRect(3, 3, 500, 26))
        Game_Name.setMouseTracking(True)
        Game_Name.setStyleSheet("QWidget {\n"
                                     "    background-color: rgb(255, 255, 255,20);\n"
                                     "    font: 15pt \"微软雅黑\";\n"
                                     "    color: rgb(255, 255, 255);\n"
                                     "     }\n"
                                     "")
        Game_Name.setText(f"{game_name}")
        Game_Name.setObjectName("Game_Name")

        pushButton_Evaluate = QtWidgets.QPushButton(frame_gamelibrary)
        pushButton_Evaluate.setGeometry(QtCore.QRect(340, 40, 75, 23))
        pushButton_Evaluate.setStyleSheet("QPushButton {\n"
                                               "         background-color: rgb(92, 138, 0);\n"
                                               "    color: rgb(255, 255, 255);\n"
                                               "     }")
        pushButton_Evaluate.setObjectName("pushButton_Evaluate")
        pushButton_Evaluate.clicked.connect(lambda :self.evaluate_game_page(game_name))
        pushButton_Evaluate.setText("评价")

        pushButton_StartGame = QtWidgets.QPushButton(frame_gamelibrary)
        pushButton_StartGame.setGeometry(QtCore.QRect(420, 40, 75, 23))
        pushButton_StartGame.setStyleSheet("QPushButton {\n"
                                                "         background-color: rgb(154, 231, 231);\n"
                                                "    color: rgb(255, 255, 255);\n"
                                                "     }")
        pushButton_StartGame.setObjectName("pushButton_StartGame")

        pushButton_Remove = QtWidgets.QPushButton(frame_gamelibrary)
        pushButton_Remove.setGeometry(QtCore.QRect(260, 40, 75, 23))
        pushButton_Remove.setStyleSheet("QPushButton {\n"
                                             "         background-color: rgb(92, 138, 0);\n"
                                             "    color: rgb(255, 255, 255);\n"
                                             "     }")
        pushButton_Remove.setObjectName("pushButton_Remove")
        pushButton_Remove.clicked.connect(lambda: self.remove_games_from_gamelirary(game_name))
        pushButton_Remove.setText("移出库")

        frame_gamelibrary.show()

    #游戏评价
    def evaluate_game_page(self, game_name):
        #初始化页面
        # 先清除之前展示的评价
        for frame in self.evaluation_frames:
            frame.deleteLater()  # 使用deleteLater()安全删除对象m
        self.evaluation_frames.clear()  # 清空列表
        self.ui.scrollAreaWidgetContents_5.update()  # 更新界面
        self.ui.stackedWidget_Window.setCurrentIndex(7)
        self.ui.success_error_Type.setCurrentIndex(0)
        self.ui.label_show_gameName.setText(f"{game_name}")
        self.ui.lineEdit_writeForWhichGame.setText(f"为 {game_name} 写一篇评测")
        self.ui.pushButton_postSure.clicked.connect(lambda: self.post_evaluate(game_name))
        self.ui.pushButton_recommend.clicked.connect(lambda: self.clicked_recommend_button())
        self.ui.pushButton_disrecommend.clicked.connect(lambda: self.clicked_disrecommend_button())

        # 连接数据库
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
        cursor = db.cursor()
        #查询游戏id
        cursor.execute(f"SELECT GAME_ID FROM game WHERE GAME_NAME = %s",(game_name,))
        game_id = cursor.fetchone()

        #查询游戏评价
        cursor.execute(f"SELECT count(*) FROM  evaluatetable WHERE GAME_ID = %s",(game_id,))
        evaluate_count= int(cursor.fetchone()[0])

        if evaluate_count:
            cursor.execute(f"SELECT e.EVALUATE, e.EVALUATE_DATE, e.SCORE, u.ACCOUNT_NUMBER FROM  evaluatetable e JOIN   user u ON e.USER_ID = u.USER_ID  WHERE   e.GAME_ID = %s",(game_id))
            all_evaluates = cursor.fetchall()
            for i in range(0, evaluate_count):
                print(f"{all_evaluates[i][0]}, {all_evaluates[i][1]}, {all_evaluates[i][2]}, {all_evaluates[i][3]}")
            self.show_game_evaluate(game_id)
        else:
            print("该游戏暂无评价")

    #发布评价
    # def post_evaluate(self, game_name):
    #     #获取新数据
    #     new_game_evaluate = self.ui.textEdit_evaluate.toPlainText()
    #
    #     # 连接数据库
    #     db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
    #     cursor = db.cursor()
    #
    #     #查询游戏id
    #     cursor.execute(f"SELECT GAME_ID FROM game WHERE GAME_NAME = %s", (game_name,))
    #     game_id_result = cursor.fetchone()
    #
    #     game_id = game_id_result[0]
    #
    #     try:
    #         #开始事务处理
    #         with db.cursor() as cursor:
    #             #插入evaluatetable表
    #             now_time = datetime.datetime.now()
    #             cursor.execute(
    #                 "INSERT INTO evaluatetable (USER_ID, GAME_ID, EVALUATE, EVALUATE_DATE, SCORE) VALUES (%s, %s, %s, %s, %s)",
    #                 (USERID, game_id, new_game_evaluate, now_time, self.new_game_score))
    #             print(f"游戏：{game_name}, 评测：{new_game_evaluate}, 是否推荐：{self.new_game_score}")
    #             db.commit()
    #             print("评测已发出")
    #     except pymysql.MySQLError as e:
    #         print(f"Database Error: {e}")
    #         db.rollback()  # 出现错误时回滚事务
    #         self.ui.success_error_Type.setCurrentIndex(2)  # 设置错误索引
    #     finally:
    #         db.close()
    #         #设置成功状态
    #         self.ui.success_error_Type.setCurrentIndex(1)
    def post_evaluate(self, game_name):
        # 获取新数据
        new_game_evaluate = self.ui.textEdit_evaluate.toPlainText()

        # 连接数据库
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
        cursor = db.cursor()

        # 查询游戏id
        cursor.execute(f"SELECT GAME_ID FROM game WHERE GAME_NAME = %s", (game_name,))
        game_id_result = cursor.fetchone()

        if game_id_result is None:
            print(f"游戏 '{game_name}' 未找到")
            self.ui.success_error_Type.setCurrentIndex(2)  # 设置错误索引
            return

        game_id = game_id_result[0]

        try:
            # 开始事务处理
            with db.cursor() as cursor:
                # 插入evaluatetable表
                now_time = datetime.datetime.now()
                cursor.execute(
                    "INSERT INTO evaluatetable (USER_ID, GAME_ID, EVALUATE, EVALUATE_DATE, SCORE) VALUES (%s, %s, %s, %s, %s)",
                    (USERID, game_id, new_game_evaluate, now_time, self.new_game_score))
                print(f"游戏：{game_name}, 评测：{new_game_evaluate}, 是否推荐：{self.new_game_score}")
                db.commit()
                print("评测已发出")

            # 设置成功状态
            self.ui.success_error_Type.setCurrentIndex(1)

            # 刷新评价界面
            self.show_game_evaluate(game_id)

        except pymysql.MySQLError as e:
            print(f"Database Error: {e}")
            db.rollback()  # 出现错误时回滚事务
            self.ui.success_error_Type.setCurrentIndex(2)  # 设置错误索引
        finally:
            db.close()

    #推荐
    def clicked_recommend_button(self):
        self.new_game_score = 1;
        print(f"推荐{self.new_game_score}")

    #不推荐
    def clicked_disrecommend_button(self):
        self.new_game_score = 0;
        print(f"不推荐{self.new_game_score}")

    #显示游戏game的所有评价
    def show_game_evaluate(self, game_id):
        self.ui.stackedWidget_Window.setCurrentIndex(7)

        #连接数据库
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
        cursor = db.cursor()
        #查询游戏评价数量
        cursor.execute(f"SELECT COUNT(*) FROM evaluatetable WHERE GAME_ID = %s",(game_id,))
        evaluate_count = int(cursor.fetchone()[0])

        cursor.execute(f"SELECT e.EVALUATE, e.EVALUATE_DATE, e.SCORE, u.ACCOUNT_NUMBER\
            FROM  evaluatetable e\
            JOIN  user u ON e.USER_ID = u.USER_ID\
            WHERE e.GAME_ID = %s", {game_id})

        all_evaluate = cursor.fetchall()
        for i in range(evaluate_count):
            print(f"{all_evaluate[i][0]}, {all_evaluate[i][1]}, {all_evaluate[i][2]}, {all_evaluate[i][3]}")
        db.close()

        all_evaluate = list(all_evaluate)
        x = 53
        y = 630

        for i in range(evaluate_count):
            frame = self.add_game_evaluate(x, y, all_evaluate[i][3], all_evaluate[i][0],
                                           all_evaluate[i][2])  # 捕获返回的frame
            self.evaluation_frames.append(frame)  # 现在可以正确添加到列表中
            y += 230
            self.update()

        self.show()

    #添加游戏评价到页面
    def add_game_evaluate(self, x, y, user_name, evaluate, score):
        frame = QFrame(parent=self.ui.scrollAreaWidgetContents_5)  # 显式指定父对象为scroll
        frame.move(x, y)
        frame.setMinimumSize(900, 200)
        frame.setMaximumSize(900, 200)
        frame.setStyleSheet("background-color: rgb(59, 59, 89);")
        frame.setObjectName("Frame")

        layoutWidget = QtWidgets.QWidget(frame)
        layoutWidget.setGeometry(QtCore.QRect(0, 0, 900, 200))
        layoutWidget.setObjectName("layoutWidget")

        frame_evaluate = QtWidgets.QVBoxLayout(layoutWidget)
        frame_evaluate.setContentsMargins(3, 3, 3, 3)
        frame_evaluate.setObjectName("Frame_Game")

        # 用户名称
        User_Name = QtWidgets.QPushButton(layoutWidget)
        User_Name.setMouseTracking(True)
        User_Name.setStyleSheet("QWidget {\n"
                                "    background-color: rgb(255, 255, 255,20);\n"
                                "    font: 15pt \"微软雅黑\";\n"
                                "    color: rgb(255, 255, 255);\n"
                                "     }\n"
                                "")
        User_Name.setText(f"{user_name}")
        User_Name.setObjectName("User_Name")
        User_Name.clicked.connect(lambda: self.show_user_page(user_name))
        frame_evaluate.addWidget(User_Name)

        # 评价栏
        Game_Evaluate = QtWidgets.QPlainTextEdit(layoutWidget)
        Game_Evaluate.setReadOnly(True)  # 设置为只读模式
        Game_Evaluate.setMouseTracking(True)
        Game_Evaluate.setStyleSheet("background-color: rgb(255, 255, 255,20);\n"
                                        "font: 10pt \"微软雅黑\";\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border:none;")
        Game_Evaluate.setLineWidth(-1)
        Game_Evaluate.setPlainText(f"{evaluate}")
        Game_Evaluate.setObjectName("Game_evaluate")
        frame_evaluate.addWidget(Game_Evaluate)

        # 推荐栏
        Game_Score = QtWidgets.QLabel(layoutWidget)
        Game_Score.setStyleSheet("background-color: rgb(255, 255, 255,20);\n"
                                 "font: 10pt \"微软雅黑\";\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "border:none;")
        if score == 1:
            Game_Score.setText("推荐")
        else:
            Game_Score.setText("不推荐")
        Game_Score.setObjectName("Game_Score")  # 注意修改了ObjectName以避免重复
        frame_evaluate.addWidget(Game_Score)  # 应该添加Game_Score而非再次添加Game_Evaluate

        frame.show()
        return frame  # 确保返回frame对象

    #刷新评价界面
    # def reload_evaluate_page(self, game_id):
    #     # 获取scrollAreaWidgetContents_Shoppingcart中的所有子部件
    #     children_widgets = self.ui.scrollAreaWidgetContents_5.findChildren(QWidget)
    #     # self.ui.emptyCartLable.setVisible(False)
    #
    #     # 遍历并删除所有子部件，但跳过名为'emptyCartLabel'的控件
    #     for child in children_widgets:
    #         if child.objectName() == "Frame":  # 假设emptyCartLabel有一个独特的objectName属性
    #             child.deleteLater()
    #
    #     self.ui.label_showAllPrice.clear()
    #
    #     # 确保所有删除操作完成
    #     QApplication.processEvents()
    #
    #     self.show_game_evaluate(game_id)

    #显示用户主页
    def show_user_page(self, user_name):
        self.ui.stackedWidget_Window.setCurrentIndex(3)

        self.ui.label_Show_FriendName.setText(f"{user_name}")

    #将游戏从库中移除
    def remove_games_from_gamelirary(self, game_name):
        # 连接数据库
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
        cursor = db.cursor()

        try:
            # 查询游戏ID
            cursor.execute(f"SELECT GAME_ID FROM game WHERE GAME_NAME = %s", (game_name,))
            game_id_result = cursor.fetchone()

            if game_id_result is None:
                print(f"游戏'{game_name}'未找到。")
                return

            game_id = game_id_result[0]

            # 删除用户对该游戏的拥有记录
            cursor.execute(f"DELETE FROM having_games WHERE USER_ID = %s AND GAME_ID = %s", (USERID, game_id))

            #创建新的订单(退款订单暂时为一对一)
            now_date = datetime.datetime.now()
            cursor.execute(
                "INSERT INTO order_for_goods (USER_ID, ORDER_STATE, ORDER_TIME) VALUES (%s, 0, %s)",
                           (USERID, now_date))
            cursor.execute(
                "SELECT ORDER_ID FROM order_for_goods WHERE USER_ID = %s AND ORDER_STATE = 0 ORDER BY ORDER_ID DESC LIMIT 1",
                (USERID,))
            new_order_id = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO order_details (ORDER_ID, GAME_ID, DETAIL_TIME, BUY_OR_REFUND) VALUES (%s, %s, %s, 2)",
                (new_order_id, game_id, now_date))

            # 更新order_for_goods表中当前用户的订单状态为已完成
            cursor.execute(
                "UPDATE order_for_goods SET ORDER_STATE = 1 WHERE USER_ID = %s AND ORDER_STATE = 0 AND ORDER_ID = %s ORDER BY ORDER_ID DESC LIMIT 1",
                (USERID, new_order_id))

            db.commit()

            # 更新界面
            self.reload_gamelibrary()

            print(f"游戏'{game_name}'已从游戏库中删除。")
        except Exception as e:
            print(f"删除游戏时发生错误: {e}")
            db.rollback()  # 发生错误时回滚事务

        finally:
            # 关闭数据库连接
            cursor.close()
            db.close()

    #刷新游戏库界面
    def reload_gamelibrary(self):
        # 获取scrollAreaWidgetContents_Gamelibrary中的所有子部件
        children_widgets = self.ui.scrollAreaWidgetContents_GameLibrary.findChildren(QWidget)

        # 遍历并删除所有子部件
        for child in children_widgets:
            child.deleteLater()

        # 确保所有删除操作完成
        QApplication.processEvents()

        # 连接数据库
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
        cursor = db.cursor()

        # 查询当前用户在havinggame表中的所有游戏ID
        cursor.execute(f"SELECT game_id FROM having_games WHERE USER_ID = %s", (USERID,))
        game_ids = cursor.fetchall()

        # 根据游戏ID查询game表中的游戏名称和简介
        game_info_list = []
        for game_id in game_ids:
            cursor.execute(f"SELECT GAME_NAME FROM game WHERE GAME_ID = %s", (game_id[0],))
            game_detail = cursor.fetchone()
            if game_detail:
                game_info_list.append(game_detail)

        db.close()

        # 重新构建界面
        x = 20
        y = 20
        for game_info in game_info_list:
            self.add_gamelibrary_page(x, y, game_info[0])
            y += 90  # 假设每个游戏框之间的垂直间距为190像素

        # 确保UI更新
        QApplication.processEvents()
        self.show()

    #显示购物车界面
    def show_personal_shoppingcart_page(self):
        self.ui.stackedWidget_Window.setCurrentIndex(5)
        # self.ui.emptyCartLable.setVisible(False)

        with pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system') as db, \
                db.cursor() as cursor:

            # 检查用户是否有未完成的订单
            cursor.execute("SELECT ORDER_ID FROM order_for_goods WHERE USER_ID = %s AND ORDER_STATE = 0", (USERID,))
            order_id = cursor.fetchone()

            # 如果有未完成订单
            if order_id:
                cursor.execute("SELECT GAME_ID FROM order_details WHERE ORDER_ID = %s",
                               (order_id[0],))
                game_already_in_cart_id = cursor.fetchall()

                # 改进逻辑：一次性获取所有游戏的名称和介绍
                game_ids_str = ', '.join(str(id[0]) for id in game_already_in_cart_id)  # 构造IN查询的字符串
                if game_ids_str:  # 如果game_ids_str非空，则执行查询
                    cursor.execute(f"SELECT GAME_NAME, PRICE FROM game WHERE GAME_ID IN ({game_ids_str})")
                    game_already_in_cart = cursor.fetchall()  # 直接获取所有游戏信息
                else:
                    print("用户暂无未完成的订单")
                    # 直接在这里处理空购物车的显示
                    # self.ui.emptyCartLable.setText("您的购物车为空。")  # 设置提示文字
                    # self.ui.emptyCartLable.setVisible(True)  # 显示空购物车的标签
                    # self.ui.emptyCartLable.setAlignment(Qt.AlignCenter)  # 可选：设置文本居中
                    # 跳过重新构建界面的循环，因为购物车是空的
                    return
            else:
                print("用户暂无未完成的订单")
                # 直接在这里处理空购物车的显示
                # self.ui.emptyCartLable.setText("您的购物车为空。")  # 设置提示文字
                # self.ui.emptyCartLable.setVisible(True)  # 显示空购物车的标签
                # self.ui.emptyCartLable.setAlignment(Qt.AlignCenter)  # 可选：设置文本居中
                 # 跳过重新构建界面的循环，因为购物车是空的
                return

        # 现在数据库连接已经安全关闭，开始处理UI逻辑
        self.ui.pushButton_KeepShopping.clicked.connect(self.show_allgames_page)
        self.ui.pushButton_Pay.clicked.connect(lambda: self.pay_for_game(order_id[0]))

        x = 10
        y = 10

        all_price = 0

        for game in game_already_in_cart:
            print(f"{game[0]}")
            self.add_shoppingcartgame_page(x, y, order_id[0], game[0], game[1])
            all_price += game[1]
            y += 110

        self.ui.label_showAllPrice.setText(f"{all_price}")

        self.show()

    #添加购物车的游戏内容
    def add_shoppingcartgame_page(self, x, y, order_id, game_name, game_price):
        frame_shopingcartgame = QFrame(parent=self.ui.scrollAreaWidgetContents_Shoppingcart)
        frame_shopingcartgame.move(x, y)
        frame_shopingcartgame.setMinimumSize(565, 100)
        frame_shopingcartgame.setMaximumSize(565, 100)
        frame_shopingcartgame.setStyleSheet("background-color: rgb(255, 255, 255,80);  ")
        frame_shopingcartgame.setObjectName('frame_' + game_name)

        pushButton_game = QtWidgets.QPushButton(frame_shopingcartgame)
        pushButton_game.setGeometry(QtCore.QRect(20, 20, 400, 50))
        pushButton_game.setStyleSheet("background-color: rgb(59, 59, 100,0);")
        pushButton_game.setText(f"{game_name}")
        pushButton_game.setObjectName('pushButton_' + game_name)

        label_ShowPrice = QtWidgets.QLabel(frame_shopingcartgame)
        label_ShowPrice.setGeometry(QtCore.QRect(483, 50, 71, 20))
        label_ShowPrice.setStyleSheet("background-color: rgb(59, 59, 100,0);")
        label_ShowPrice.setText(f"{game_price}")
        label_ShowPrice.setObjectName('label_ShowPrice_' + game_name)

        pushButton_Remove = QtWidgets.QPushButton(frame_shopingcartgame)
        pushButton_Remove.setGeometry(QtCore.QRect(484, 73, 71, 20))
        pushButton_Remove.setStyleSheet("background-color: rgb(59, 59, 100,0);")
        pushButton_Remove.setObjectName('label_Remove_' + game_name)
        pushButton_Remove.clicked.connect(lambda: self.remove_games_from_shoppingcart(order_id, game_name))
        pushButton_Remove.setText("移出购物车")
        frame_shopingcartgame.show()

    #将游戏从购物车中移除
    def remove_games_from_shoppingcart(self, order_id, game_name):
        try:
            # 连接数据库
            db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
            cursor = db.cursor()

            # 根据game_name获取game_id
            cursor.execute("SELECT GAME_ID FROM game WHERE GAME_NAME = %s", (game_name,))
            game_id_result = cursor.fetchone()
            if game_id_result is None:
                print(f"Game with name '{game_name}' not found.")
                return

            game_id = game_id_result[0]

            # 使用order_id和game_id从ORDER_FOR_GOODS表中删除记录
            cursor.execute("DELETE FROM order_details WHERE ORDER_ID = %s AND GAME_ID = %s", (order_id, game_id))
            deleted_rows = cursor.rowcount
            if deleted_rows > 0:
                print(f"Deleted {deleted_rows} record(s) from ORDER_FOR_GOODS for game '{game_name}'.")
            else:
                print(f"No records to delete for game '{game_name}' and USER_ID '{USERID}'.")

            # 提交事务
            db.commit()

        except Exception as e:
            print(f"An error occurred: {e}")
            # 发生错误时回滚事务
            db.rollback()

        finally:
            # 关闭数据库连接
            cursor.close()
            db.close()

        QTimer.singleShot(0, lambda: self.reload_shopping_cart(order_id))

    #刷新购物车界面
    def reload_shopping_cart(self, order_id):
        # 获取scrollAreaWidgetContents_Shoppingcart中的所有子部件
        children_widgets = self.ui.scrollAreaWidgetContents_Shoppingcart.findChildren(QWidget)

        # 遍历并删除所有子部件，但跳过名为'emptyCartLabel'的控件
        for child in children_widgets:
            if child.objectName() != "emptyCartLabel":
                child.deleteLater()

        self.ui.label_showAllPrice.clear()

        # 确保所有删除操作完成
        QApplication.processEvents()

        # 连接数据库并重新获取购物车中的游戏
        with pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system') as db, \
                db.cursor() as cursor:

            # 检查用户是否有未完成的订单
            cursor.execute("SELECT ORDER_ID FROM order_for_goods WHERE USER_ID = %s AND ORDER_STATE = 0", (USERID,))
            order_id = cursor.fetchone()

            # 初始化总金额
            all_price = 0

            # 如果有未完成订单
            if order_id:
                cursor.execute("SELECT GAME_ID FROM order_details WHERE ORDER_ID = %s",
                               (order_id[0],))
                game_already_in_cart_id = cursor.fetchall()

                # 构造游戏ID列表
                game_ids_str = ', '.join(
                    str(id[0]) for id in game_already_in_cart_id) if game_already_in_cart_id else ''

                if game_ids_str:  # 如果购物车不为空
                    # 查询游戏名称和价格
                    cursor.execute(f"SELECT GAME_NAME, PRICE FROM game WHERE GAME_ID IN ({game_ids_str})")
                    game_already_in_cart = cursor.fetchall()

                    # 重新构建界面
                    x = 10
                    y = 10
                    for game_info in game_already_in_cart:
                        game_name, game_price = game_info
                        self.add_shoppingcartgame_page(x, y, order_id[0], game_name, game_price)
                        all_price += float(game_price)  # 累加价格（确保价格是数值类型）
                        y += 110

                    # 更新总金额显示
                    self.ui.label_showAllPrice.setText(f"{all_price}")
                else:
                    # 购物车为空，显示空提示
                    self.ui.label_showAllPrice.setText("0")
                    print("用户购物车为空")
                    # 可选：显示空购物车提示
                    # self.ui.emptyCartLable.setText("您的购物车为空。")
                    # self.ui.emptyCartLable.setVisible(True)
                    # self.ui.emptyCartLable.setAlignment(Qt.AlignCenter)
            else:
                # 没有未完成订单，显示空提示
                self.ui.label_showAllPrice.setText("0")
                print("用户暂无未完成的订单")
                # 可选：显示空购物车提示
                # self.ui.emptyCartLable.setText("您的购物车为空。")
                # self.ui.emptyCartLable.setVisible(True)
                # self.ui.emptyCartLable.setAlignment(Qt.AlignCenter)

        # 确保UI更新
        QApplication.processEvents()
        self.show()

    #购买游戏操作实现
    def pay_for_game(self, order_id):
        """
           处理用户支付操作，将当前用户的购物车中所有游戏状态更新为已购买，
           并将这些游戏记录添加到用户的游戏库中。
           """
        try:
            # 连接数据库
            with pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system') as db, \
                    db.cursor() as cursor:

                # 获取当前用户购物车中所有待支付的游戏ID
                cursor.execute("SELECT GAME_ID FROM order_details WHERE ORDER_ID = %s AND BUY_OR_REFUND = 0",
                               (order_id,))
                purchased_game_ids = cursor.fetchall()

                #更新ordder_details中的数据
                for game_id in purchased_game_ids:
                    cursor.execute(
                        "UPDATE order_details SET BUY_OR_REFUND = 1 WHERE GAME_ID = %s AND BUY_OR_REFUND = 0 AND ORDER_ID = %s ORDER BY ORDER_ID DESC LIMIT 1",
                        (game_id[0], order_id))

                # 更新order_for_goods表中当前用户的订单状态为已完成
                cursor.execute(
                    "UPDATE order_for_goods SET ORDER_STATE = 1 WHERE USER_ID = %s AND ORDER_STATE = 0 AND ORDER_ID = %s ORDER BY ORDER_ID DESC LIMIT 1",
                    (USERID, order_id))

                # 将这些游戏ID插入到having_games表中
                # 获取当前时间
                now_time = datetime.datetime.now()
                for game_id in purchased_game_ids:
                    cursor.execute("INSERT IGNORE INTO having_games (USER_ID, GAME_ID, BUY_TIME) VALUES (%s, %s, %s)",
                                   (USERID, game_id[0], now_time))
                # 提交事务
                db.commit()
                print("支付成功，购物车中的游戏已更新为已购买状态，并已添加到游戏库。")

        except Exception as e:
            print(f"支付过程中发生错误: {e}")
            # 如果有异常，回滚事务
            if 'db' in locals():
                db.rollback()

        finally:
            # 由于使用了with语句，这里的关闭操作是多余的，但保持逻辑完整性
            # 实际上不需要手动关闭连接和游标
            pass

        #更新购物车界面
        QTimer.singleShot(0, lambda: self.reload_shopping_cart(order_id))

    #测试接口函数
    def test(self, testname):
        print(f"{testname}")


class MainManufacturerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ManufacturerWindow()  # 注意这里是实例化对象
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.success_error_Type.setCurrentIndex(0)
        # 设置窗口无边框及透明背景
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 窗口居中
        self.center()

        # 添加退出按钮
        exit_button = QPushButton(self)
        exit_button.setText("X")
        exit_button.setGeometry(QtCore.QRect(self.width() - 50, 10, 40, 40))
        exit_button.setStyleSheet("""
                   QPushButton {
                       background-color: rgba(255, 255, 255, 50);
                       color: white;
                       font: 14pt "微软雅黑";
                       border-radius: 5px;
                   }
                   QPushButton:hover {
                       background-color: rgba(255, 0, 0, 100);
                   }
               """)
        exit_button.clicked.connect(self.close)

        #按钮绑定
        #跳转发布游戏界面按钮绑定
        self.ui.pushButton_releaseGame.clicked.connect(self.show_releasegame_page)
        #跳转主页界面按钮绑定
        self.ui.pushButton_HomePage.clicked.connect(self.show_homepage)
        #跳转游戏管理界面按钮绑定
        self.ui.pushButton_manageGame.clicked.connect(self.show_managegame_page)

        #显示信息
        #厂商名称
        # 连接数据库
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
        cursor = db.cursor()

        cursor.execute("SELECT ACCOUNT_NUMBER FROM manufacturer WHERE MANUFACTURER_ID = %s",(MANUFACTURERID))
        manufacturer_name = cursor.fetchone()[0]
        self.ui.message1.setText(f"{manufacturer_name}")

        cursor.execute("SELECT COUNT(*) FROM game WHERE MANUFACTURER_ID = %s",(MANUFACTURERID))
        game_count = int(cursor.fetchone()[0])
        self.ui.message3.setText(f"{game_count}")

    #居中显示
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    #显示厂商主页
    def show_homepage(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.show()

    #显示发布游戏界面
    def show_releasegame_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.pushButton_releaseSure.clicked.connect(self.release_game)
        self.show()

    #显示管理游戏界面
    def show_managegame_page(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        # 连接数据库
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
        cursor = db.cursor()

        # 查询当前厂商拥有的所有游戏
        cursor.execute(f"SELECT GAME_NAME FROM game WHERE MANUFACTURER_ID = %s", (MANUFACTURERID))
        all_gamename = cursor.fetchall()

        cursor.close()
        db.close()

        x = 40
        y = 20
        for gamename in all_gamename:
            print(f"{gamename}")
            self.add_managegame_page(x, y, gamename)
            y += 80

        self.show()

    #发布游戏功能实现
    def release_game(self):
        # 获取用户输入
        new_gamename = self.ui.lineEdit_gameName.text()
        new_gameintroduction = self.ui.textEdit_gameIntroduction.toPlainText()
        new_gametype1 = self.ui.lineEdit_gameType1.text()
        new_gametype2 = self.ui.lineEdit_gameType2.text()
        new_gametype3 = self.ui.lineEdit_gameType3.text()
        new_gameprice = self.ui.lineEdit_gamePrice.text()

        # 连接数据库
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
        cursor = db.cursor()

        try:
            # 1. 检查游戏名是否重复
            cursor.execute("SELECT COUNT(*) FROM game WHERE GAME_NAME = %s", (new_gamename,))
            if cursor.fetchone()[0] > 0:
                print(f"游戏名'{new_gamename}'已存在")
                self.ui.success_error_Type.setCurrentIndex(3)  # 错误：游戏名重复
                return

            # 2. 检查必填字段（游戏名、简介、价格）
            if not all([new_gamename, new_gameintroduction, new_gameprice]):
                print("请填写游戏名、简介和价格")
                self.ui.success_error_Type.setCurrentIndex(2)  # 错误：必填字段为空
                return

            # 3. 检查至少填写一个游戏类型
            game_types = [t for t in [new_gametype1, new_gametype2, new_gametype3] if t.strip()]
            if not game_types:
                print("请至少填写一个游戏类型")
                self.ui.success_error_Type.setCurrentIndex(2)  # 错误：类型为空
                return

            # 4. 插入游戏数据
            now_time = datetime.datetime.now()
            cursor.execute(
                "INSERT INTO game (GAME_NAME, MANUFACTURER_ID, INTRODUCTION, PRICE, PUBLISH_TIME) "
                "VALUES (%s, %s, %s, %s, %s)",
                (new_gamename, MANUFACTURERID, new_gameintroduction, new_gameprice, now_time)
            )

            # 5. 获取游戏ID并插入类型（仅非空类型）
            game_id = cursor.lastrowid
            for gametype in game_types:
                cursor.execute(
                    "INSERT INTO game_to_type (GAME_ID, TYPE_NAME) VALUES (%s, %s)",
                    (game_id, gametype)
                )

            db.commit()
            print("游戏发布成功！")
            self.ui.success_error_Type.setCurrentIndex(1)  # 成功提示

        except pymysql.MySQLError as e:
            print(f"数据库错误: {e}")
            db.rollback()
            self.ui.success_error_Type.setCurrentIndex(3)  # 数据库错误
        finally:
            db.close()

    #添加厂商游戏到界面
    def add_managegame_page(self, x, y, gamename):
        # 创建游戏条目框架
        frame_applicationuser = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents_manageGame)
        frame_applicationuser.move(x, y)
        frame_applicationuser.setMinimumSize(700, 70)
        frame_applicationuser.setMaximumSize(700, 70)
        frame_applicationuser.setStyleSheet("""
            background-color: rgb(59, 59, 89);
            border-radius: 8px;
        """)
        frame_applicationuser.setObjectName("frame")

        # 显示游戏名称（处理元组格式）
        Game_Name = QtWidgets.QLabel(frame_applicationuser)
        Game_Name.setGeometry(QtCore.QRect(20, 15, 500, 40))  # 调整位置和大小
        Game_Name.setStyleSheet("""
            QLabel {
                font: 16pt "微软雅黑";
                color: white;
                background: transparent;
            }
        """)

        # 从元组中提取游戏名（去掉括号和逗号）
        if isinstance(gamename, tuple) and len(gamename) > 0:
            display_name = str(gamename[0])
        else:
            display_name = str(gamename)

        Game_Name.setText(display_name)
        Game_Name.setObjectName("Game_Name")
        # pushButton_Introduction = QtWidgets.QPushButton(frame_applicationuser)
        # pushButton_Introduction.setGeometry(QtCore.QRect(530, 40, 75, 20))
        # pushButton_Introduction.setStyleSheet("QPushButton {\n"
        #                                "         background-color: rgb(92, 138, 0);\n"
        #                                "    color: rgb(255, 255, 255);\n"
        #                                "     }")
        # pushButton_Introduction.setObjectName("pushButton_Agree")
        # # pushButton_Introduction.clicked.connect(lambda: self.agree_friend(username)) //这个功能不想做了
        # pushButton_Introduction.setText("详情")

        # 下架按钮
        pushButton_Delete = QtWidgets.QPushButton(frame_applicationuser)
        pushButton_Delete.setGeometry(QtCore.QRect(550, 20, 120, 30))  # 调整位置和大小
        pushButton_Delete.setStyleSheet("""
            QPushButton {
                background-color: rgb(100, 180, 180);
                color: white;
                border-radius: 5px;
                font: 12pt "微软雅黑";
            }
            QPushButton:hover {
                background-color: rgb(120, 200, 200);
            }
        """)
        pushButton_Delete.setObjectName("pushButton_Reject")
        pushButton_Delete.clicked.connect(lambda: self.delete_game(gamename))
        pushButton_Delete.setText("下架")

        frame_applicationuser.show()

    def delete_game(self, game_name):
        # 连接数据库
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
        cursor = db.cursor()

        try:
            #查询游戏id
            cursor.execute(f"SELECT GAME_ID FROM game WHERE GAME_NAME = %s", (game_name,))
            game_id_result = cursor.fetchone()

            if game_id_result is None:
                print(f"游戏'{game_name}'未找到。")
                return

            game_id = game_id_result[0]

            #删除所有用户对该游戏的评价
            cursor.execute(f"DELETE FROM evaluatetable WHERE GAME_ID = %s", (game_id))
            #删除游戏在订单上的信息
            cursor.execute(f"DELETE FROM order_details WHERE GAME_ID = %s", (game_id))
            # 删除所有用户对该游戏的拥有记录
            cursor.execute(f"DELETE FROM having_games WHERE GAME_ID = %s", (game_id))
            #删除游戏拥有的标签信息
            cursor.execute(f"DELETE FROM game_to_type WHERE GAME_ID = %s", (game_id))
            #删除厂商对游戏的拥有信息
            cursor.execute(f"DELETE FROM game WHERE GAME_ID = %s", (game_id))
            db.commit()
        except pymysql.MySQLError as e:
            print(f"Database Error: {e}")
            db.rollback()
        finally:
            db.close()
        # 更新界面
        self.reload_managegame()

        print(f"游戏'{game_name}'已从游戏库中删除。")

    #刷新游戏管理界面
    def reload_managegame(self):
        # 获取scrollAreaWidgetContents_Gamelibrary中的所有子部件
        children_widgets = self.ui.scrollAreaWidgetContents_manageGame.findChildren(QWidget)

        # 遍历并删除所有子部件
        for child in children_widgets:
            child.deleteLater()

        # 确保所有删除操作完成
        QApplication.processEvents()

        # 连接数据库
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
        cursor = db.cursor()

        #查询当前厂商拥有的所有游戏
        cursor.execute(f"SELECT GAME_NAME FROM game WHERE MANUFACTURER_ID = %s",(MANUFACTURERID))
        all_gamename = cursor.fetchall()
        all_gamename = list(all_gamename)
        cursor.close()
        db.close()

        x = 40
        y = 20
        for gamename in all_gamename:
            print(f"{gamename}")
            self.add_managegame_page(x, y, gamename)
            y += 80

        self.show()


class GameEvaluationWindow(QtWidgets.QMainWindow):
    def __init__(self, game_id, game_name):
        super().__init__()
        self.game_id = game_id
        self.game_name = game_name

        self.setWindowTitle(f"{game_name} - 游戏评价")
        self.resize(800, 600)

        # 主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)

        # 标题
        title_label = QLabel(f"《{game_name}》的游戏评价")
        title_label.setStyleSheet("font: 20pt '微软雅黑'; color: white;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 评价统计信息
        stats_frame = QFrame()
        stats_frame.setStyleSheet("background-color: rgb(59, 59, 89);")
        stats_layout = QHBoxLayout(stats_frame)

        # 添加统计信息组件
        self.total_reviews_label = QLabel("总评价数: 0")
        self.total_reviews_label.setStyleSheet("color: white;")
        stats_layout.addWidget(self.total_reviews_label)

        self.positive_rate_label = QLabel("好评率: 0%")
        self.positive_rate_label.setStyleSheet("color: white;")
        stats_layout.addWidget(self.positive_rate_label)

        stats_layout.addStretch()
        main_layout.addWidget(stats_frame)

        # 评价列表滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(scroll_area)

        # 加载评价数据
        self.load_evaluations()

        # 窗口样式
        self.setStyleSheet("background-color: rgb(38, 38, 38);")

    def load_evaluations(self):
        # 清除旧评价
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().deleteLater()

        try:
            db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='game_system')
            cursor = db.cursor()

            # 查询评价总数和好评率
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN SCORE = 1 THEN 1 ELSE 0 END) as positive,
                    SUM(CASE WHEN SCORE = 0 THEN 1 ELSE 0 END) as negative
                FROM evaluatetable 
                WHERE GAME_ID = %s
            """, (self.game_id,))

            stats = cursor.fetchone()
            total = stats[0]
            positive = stats[1]
            negative = stats[2]

            if total > 0:
                positive_rate = round(positive / total * 100, 1)
            else:
                positive_rate = 0

            self.total_reviews_label.setText(f"总评价数: {total}")
            self.positive_rate_label.setText(f"好评率: {positive_rate}%")

            # 查询具体评价内容
            cursor.execute("""
                SELECT e.EVALUATE, e.EVALUATE_DATE, e.SCORE, u.ACCOUNT_NUMBER 
                FROM evaluatetable e
                JOIN user u ON e.USER_ID = u.USER_ID
                WHERE e.GAME_ID = %s
                ORDER BY e.EVALUATE_DATE DESC
            """, (self.game_id,))

            evaluations = cursor.fetchall()

            for eval in evaluations:
                self.add_evaluation_item(
                    eval[3],  # 用户名
                    eval[0],  # 评价内容
                    eval[1],  # 评价日期
                    eval[2]  # 评分
                )

        except pymysql.MySQLError as e:
            print(f"Database Error: {e}")
        finally:
            db.close()

    def add_evaluation_item(self, username, content, date, score):
        frame = QFrame()
        frame.setStyleSheet("background-color: rgb(59, 59, 89); border-radius: 5px;")
        frame.setMinimumHeight(120)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)

        # 用户信息和日期
        user_layout = QHBoxLayout()

        user_label = QLabel(username)
        user_label.setStyleSheet("color: white; font-weight: bold;")
        user_layout.addWidget(user_label)

        user_layout.addStretch()

        date_label = QLabel(date.strftime("%Y-%m-%d %H:%M"))
        date_label.setStyleSheet("color: #AAAAAA;")
        user_layout.addWidget(date_label)

        layout.addLayout(user_layout)

        # 评价内容
        content_text = QPlainTextEdit()
        content_text.setPlainText(content)
        content_text.setReadOnly(True)
        content_text.setStyleSheet("""
            QPlainTextEdit {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: none;
                padding: 5px;
            }
        """)
        content_text.setMaximumHeight(80)
        layout.addWidget(content_text)

        # 评分
        score_label = QLabel("推荐" if score == 1 else "不推荐")
        score_label.setStyleSheet("color: {};".format("#4CAF50" if score == 1 else "#F44336"))
        layout.addWidget(score_label)

        self.scroll_layout.addWidget(frame)


if __name__ == '__main__':
    # 启用高DPI缩放
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    win = LogInWindow()
    sys.exit(app.exec_())