import win32gui
import time
from PIL import ImageGrab, Image, ImageChops
import numpy as np
import pyautogui
import cv2
from skimage.metrics import structural_similarity as compare_ssim
import os


def main():

    wdname = '宠物连连看3.1H5_宠物连连看3.1H5html5游戏在线玩_4399h5游戏-4399在线玩 - Google Chrome'
    demo = GameAssist(wdname)
    # demo.img2mun()
    # demo.get_small_pic()
    demo.start()


class GameAssist:

    def __init__(self, wdname):
        """初始化"""
        self.hwnd = win32gui.FindWindow(None, wdname)
        if not self.hwnd:
            print("窗口找不到，请确认窗口句柄名称：【%s】" % wdname)
            exit()
        win32gui.SetForegroundWindow(self.hwnd)

        self.im_width = 58
        self.win_top = 331
        self.win_left = 401
        self.win_bottom = 911
        self.win_right = 1213
        self.im2num_arr = self.img2mun()
        pyautogui.FAILSAFE = True

    def get_small_pic(self):
        # img_cap = ImageGrab(bbox=(401,331,1213,911))
        img_cap = pyautogui.screenshot(region=(self.win_left, self.win_top, 812, 580))
        img_cap.save('imgcut\\shotcut.png')
        for i in range(14):
            for j in range(10):
                filename = 'imgcut\\{}_{}.png'.format(i+1, j+1)
                img_top = i*self.im_width+4
                img_left = j*self.im_width+4
                img_bottom = (i+1)*self.im_width-6
                img_right = (j+1)*self.im_width-6
                img = img_cap.crop((img_top, img_left, img_bottom, img_right))
                img.save(filename)

    def img2mun(self):
        arr = np.zeros((12, 16), dtype=np.int32)
        print(arr)
        folder_path = os.path.join(os.getcwd(), 'img')
        file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
        # print(file_count)
        image_type_list = []

        for i in range(1, file_count+1):
            image_type_list.append(i)
            file = 'img\\{}.png'.format(i)
            alll_ocation = pyautogui.locateAllOnScreen(file, confidence=0.92)
            all_locations = list(alll_ocation)
            for location in all_locations:
                x = location.top
                y = location.left
                x1 = (x - self.win_top) // self.im_width
                y1 = (y - self.win_left) // self.im_width
                arr[x1+1][y1+1] = i
        # print(image_type_list)
        # print(arr)
        # self.im2num_arr = arr

        return arr

    def is_all_zero(self, arr):
        for i in range(1, 11):
            for j in range(1, 15):
                if arr[i][j] != 0:
                    return False
        return True

    def is_reachable(self, x1, y1, x2, y2):
        if self.im2num_arr[x1][y1] != self.im2num_arr[x2][y2]:
            return False
        list1 = self.get_direct_connect_list(x1, y1)
        list2 = self.get_direct_connect_list(x2, y2)

        for x1, y1 in list1:
            for x2, y2 in list2:
                if self.is_direct_connect(x1, y1, x2, y2):
                    return True
        return False

    def get_direct_connect_list(self, x, y):
        plist = []

        for px in range(0, 12):
            for py in range(0, 16):
                if self.im2num_arr[px][py] == 0 and self.is_direct_connect(x, y, px, py):
                    plist.append([px, py])

        return plist

    def is_direct_connect(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return False

        if (x1 != x2) and (y1 != y2):
            return False

        if x1 == x2 and self.is_row_connect(x1, y1, y2):
            return True

        if y1 == y2 and self.is_col_connect(y1, x1, x2):
            return True

        return False

    def is_row_connect(self, x, y1, y2):
        min_y = min(y1, y2)
        max_y = max(y1, y2)

        if abs(max_y - min_y) == 1:
            return True

        for y in range(min_y + 1, max_y):
            if self.im2num_arr[x][y] != 0:
                return False

        return True

    def is_col_connect(self, y, x1, x2):
        max_x = max(x1, x2)
        min_x = min(x1, x2)

        if abs(max_x - min_x) == 1:
            return True

        for x in range(min_x + 1, max_x):
            if self.im2num_arr[x][y] != 0:
                return False

        return True

    def click_and_set_zero(self, x1, y1, x2, y2):
        p1_x = int(self.win_left + (y1 - 1) * self.im_width + self.im_width/2)
        p1_y = int(self.win_top + (x1 - 1) * self.im_width + self.im_width/2)

        p2_x = int(self.win_left + (y2 - 1) * self.im_width + self.im_width/2)
        p2_y = int(self.win_top + (x2 - 1) * self.im_width + self.im_width/2)

        time.sleep(0.2)
        pyautogui.click(p1_x, p1_y)

        # self.mouse.click(p1_x, p1_y)
        time.sleep(0.2)
        pyautogui.click(p2_x, p2_y)
        # self.mouse.click(p2_x, p2_y)
        print("消除：(%d, %d) (%d, %d)" % (x1, y1, x2, y2))

        # self.im2num_arr[x1][y1] = 0
        for i in range(y1, 15):
            self.im2num_arr[x1][i] = self.im2num_arr[x1][i + 1]
        # self.im2num_arr[x2][y2] = 0
        for j in range(y2, 15):
            self.im2num_arr[x2][j] = self.im2num_arr[x2][j + 1]
        # exit()

    def start(self):
        # 1、先截取游戏区域大图，然后分切每个小图
        # image_list = self.screenshot()
        # self.image2num(image_list)
        print(self.im2num_arr)

        while not self.is_all_zero(self.im2num_arr):
            # if pyautogui.FAILSAFE:
            #     break
            for x1 in range(11, 0,-1):
                for y1 in range(15, 0,-1):
                    if self.im2num_arr[x1][y1] == 0:
                        continue

                    for x2 in range(11, 0,-1):
                        for y2 in range(15, 0,-1):
                            # 跳过为0 或者同一个
                            if self.im2num_arr[x2][y2] == 0 or (x1 == x2 and y1 == y2):
                                continue
                            if self.is_reachable(x1, y1, x2, y2):
                                self.click_and_set_zero(x1, y1, x2, y2)
                                print(self.im2num_arr)


if __name__ == '__main__':
    main()
