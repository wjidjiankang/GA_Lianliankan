import win32gui
import time
from PIL import ImageGrab, Image,ImageChops
import numpy as np
import operator
# from pymouse import PyMouse
import pyautogui
import cv2
# from skimage.measure import compare_ssim
from skimage.metrics import structural_similarity as compare_ssim


def main():

    # wdname = '宠物连连看3.1H5_宠物连连看3.1H5html5游戏在线玩_4399h5游戏-4399在线玩 - 个人 - Microsoft Edge'
    wdname = '宠物连连看3.1H5_宠物连连看3.1H5html5游戏在线玩_4399h5游戏-4399在线玩 - Google Chrome'
    # wdname=  '果蔬连连看H5_果蔬连连看H5html5游戏在线玩_4399h5游戏-4399在线玩 - Google Chrome'

    demo = GameAssist(wdname)
    # demo.start()
    # demo.screenshot()
    # list1 = [0, 1, 2, 3]
    # demo.image2num(list1)
    demo.start()



class GameAssist:

    def __init__(self, wdname):

        """初始化"""
        self.hwnd = win32gui.FindWindow(None, wdname)
        if not self.hwnd:
            print("窗口找不到，请确认窗口句柄名称：【%s】" % wdname)
            exit()
        win32gui.SetForegroundWindow(self.hwnd)
        img = ImageGrab.grab(bbox=(0,0,1920,1080))
        img.save('screenshot.png')
        self.im2num_arr = []
        self.screen_left_and_right_point = (402, 332, 1214, 912)
        self.im_width = 52
        self.interval_x = 58.2
        self.interval_y = 58.15
        # img = ImageGrab.grab(bbox=(self.screen_left_and_right_point))

        # self.mouse = PyMouse()
        # self.mouse = pyautogui.click()

    def screenshot(self):
        image = ImageGrab.grab(bbox=self.screen_left_and_right_point)
        image.save('lianliankan.png')
        image_list = {}
        # image_list = []
        # offset = self.im_width
        for x in range(10):
            # image_list[x]= []
            image_list[x] = {}
            for y in range(14):
                # top = x*(self.im_width+self.interval)
                # left = y*(self.im_width+self.interval)
                # right = left+self.im_width
                # bottom = top+self.im_width
                # im = image.crop((left, top, right, bottom))
                centerx = 27+(self.interval_x*x)
                centery = 27+(self.interval_y*y)
                top = centerx-self.im_width/2
                left = centery - self.im_width/2
                right = left + self.im_width
                bottom = top + self.im_width
                im = image.crop((left, top, right, bottom))
                im.save('im{}{}.png'.format(x,y))
                image_list[x][y] = im
        return image_list

    def image2num(self, imagelist):
        arr = np.zeros((12, 16), dtype=np.int32)
        print(arr)
        # print(image_list)
        image_type_list = []
        for i in range(len(imagelist)):
            for j in range(len(imagelist[0])):
                im = imagelist[i][j]
                index = self.get_index(im, image_type_list)
                if index < 0:
                    image_type_list.append(im)
                    arr[i+1][j+1] = len(image_type_list)
                else:
                    arr[i + 1][j + 1] = index+1
        print('图标数量：', len(image_type_list))
        self.im2num_arr = arr
        return arr

    def get_index(self, im, im_list):
        for i in range(len(im_list)):
            if self.is_match(im, im_list[i]):
                return i
        return -1

    def is_match(self, im1, im2):
        image1 = im1.resize((20, 20), Image.Resampling.LANCZOS).convert('L')
        image2 = im2.resize((20, 20), Image.Resampling.LANCZOS).convert('L')
        pixels1 = list(image1.getdata())
        pixels2 = list(image2.getdata())

        avg1 = sum(pixels1)/len(pixels1)
        avg2 = sum(pixels2)/len(pixels2)

        hash1 = "".join(map(lambda p: "1" if p > avg1 else "0", pixels1))
        hash2 = "".join(map(lambda p: "1" if p > avg2 else "0", pixels2))

        match = sum(map(operator.ne, hash1, hash2))
        print(match)
        # 阀值设为10
        return match < 40

    def is_match2(self,im1,im2):
        image1 = im1.resize((20, 20), Image.Resampling.LANCZOS).convert('L')
        image2 = im2.resize((20, 20), Image.Resampling.LANCZOS).convert('L')

        diff = ImageChops.difference(image1, image2)
        # 计算差异像素的数量
        diff_pixels = diff.getdata().count((255, 255, 255, 255))
        # 计算相似度
        similarity = (255 - diff_pixels) / 255
        return similarity<10

    def is_match3(self,im1,im2):
        # 将图像转换为灰度图像
        image1 = im1.convert('L')
        image2 = im2.convert('L')

        # 将灰度图像转换为 NumPy 数组
        array1 = np.array(image1)
        array2 = np.array(image2)

        # 计算 MSE（均方误差）
        mse = np.mean((array1 - array2) ** 2)

        return mse<70

    def is_match4(self,im1,im2):
        # img1_gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        # img2_gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

        # 计算两个图像的差异
        # ssim = cv2.compareSSIM(img1_gray, img2_gray)
        ssim = compare_ssim(im1,im2)
        return ssim>0.9

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

        for x1,y1 in list1:
            for x2,y2 in list2:
                if self.is_direct_connect(x1,y1,x2,y2):
                    return True
        return False


    def get_direct_connect_list(self, x, y):
        plist = []
        for px in range(12):
            for py in range(16):
                if self.im2num_arr[px][py] ==0 and self.is_direct_connect(x,y,px,py):
                    plist.append([px,py])
        return plist

    def is_direct_connect(self,x1,y1,x2,y2):
        if x1 == x2 and y1==y2:
            return False
        if x1 != x2 and y1 != y2:
            return False
        if x1 ==x2 and self.is_row_connect(x1,y1,y2):
            return True
        if y1 ==y2 and self.is_col_connect(y1,x1,x2):
            return True
        return False


    def is_row_connect(self,x,y1,y2):
        min_y = min(y1,y2)
        max_y = max(y1,y2)
        if max_y - min_y ==1:
            return True
        for y0 in range(min_y+1,max_y):
            if self.im2num_arr[x][y0] !=0:
                return False
        return True


    def is_col_connect(self,y,x1,x2):
        max_x = max(x1,x2)
        min_x = min(x1,x2)
        if max_x - min_x ==1:
            return True
        for x0 in range(min_x+1,max_x):
            if self.im2num_arr[x0][y] !=0:
                return False
        return True

    def click_and_set_zero(self,x1,y1,x2,y2):
        p1_x = int(self.screen_left_and_right_point[0] + (y1 - 1) * (self.interval_x) + (self.interval_x / 2))
        p1_y = int(self.screen_left_and_right_point[1] + (x1 - 1) * (self.interval_x) + (self.interval_x / 2))

        p2_x = int(self.screen_left_and_right_point[0] + (y2 - 1) * (self.interval_x)+ (self.interval_x / 2))
        p2_y = int(self.screen_left_and_right_point[1] + (x2 - 1) * (self.interval_x) + (self.interval_x / 2))

        time.sleep(0.2)
        pyautogui.click(p1_x, p1_y)

        # self.mouse.click(p1_x, p1_y)
        time.sleep(0.2)
        pyautogui.click(p2_x, p2_y)
        # self.mouse.click(p2_x, p2_y)

        self.im2num_arr[x1][y1] = 0
        self.im2num_arr[x2][y2] = 0

        print("消除：(%d, %d) (%d, %d)" % (x1, y1, x2, y2))
        # exit()



    def start(self):
        # 1、先截取游戏区域大图，然后分切每个小图

        image_list = self.screenshot()
        self.image2num(image_list)

        print(self.im2num_arr)

        while not self.is_all_zero(self.im2num_arr):
            for x1 in range(1, 11):
                for y1 in range(1, 15):
                    if self.im2num_arr[x1][y1] == 0:
                        continue

                    for x2 in range(1, 11):
                        for y2 in range(1, 15):
            # 跳过为0 或者同一个
                            if self.im2num_arr[x2][y2] == 0 or (x1 == x2 and y1 == y2):
                                continue
                            if self.is_reachable(x1, y1, x2, y2):
                                self.click_and_set_zero(x1, y1, x2, y2)


if __name__ == '__main__':
    main()
