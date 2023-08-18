def click_and_set_zero(self, x1, y1, x2, y2):
    p1_x = int(self.win_left + (y1 - 1) * self.im_width + self.im_width / 2)
    p1_y = int(self.win_top + (x1 - 1) * self.im_width + self.im_width / 2)

    p2_x = int(self.win_left + (y2 - 1) * self.im_width + self.im_width / 2)
    p2_y = int(self.win_top + (x2 - 1) * self.im_width + self.im_width / 2)

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