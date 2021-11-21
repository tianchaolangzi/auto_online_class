from selenium import webdriver
from selenium.webdriver.common.by import By
import pytesseract
from PIL import Image
from time import sleep
import re


def is_time_enough(text):
    # text = '需要学习17分钟，已学习17分钟'
    # 本项最少需要学习17分钟，最多记录17分钟，您已经学习17分钟。
    need_time = float(re.search(r'需要学习(\d+)分钟', text).group(1))
    learned_time = float(re.search(r'已经*学习(\d+)分钟', text).group(1))
    if need_time <= learned_time:
        return True
    else:
        return False


def watch_video(browser):
    sleep(2)
    print("start watching")
    text = browser.find_element(By.XPATH, '''//*[@id="itemProgress"]''').text
    while not is_time_enough(text):
        sleep(60)
        text = browser.find_element(By.XPATH, '''//*[@id="itemProgress"]''').text
    print("stop watching")


def imgcode_auto_input(browser):
    # 识别验证码
    input_imgcode = browser.find_element(By.XPATH, '''// *[ @ id = "randomCode"]''')
    input_imgcode.send_keys("")
    sleep(1)
    img = browser.find_element(By.XPATH, '''//*[@id="imgCode"]''')
    browser.save_screenshot('screenshot.png')
    left = img.location['x']
    top = img.location['y']
    right = img.size['width'] + left
    height = img.size['height'] + top
    screenshot = Image.open('screenshot.png')
    imgcode = screenshot.crop((left, top, right, height))
    imgcode.save('imgcode.png')  # 这里就是截取到的验证码图片
    image1 = Image.open('imgcode.png')
    text = pytesseract.image_to_string(image1)
    input_imgcode.send_keys(text)


def loop_floor(browser):
    try:
        videoList1 = browser.find_element(By.XPATH, '''/html/body/div[4]/div[2]'''
                                          ).find_elements(By.CLASS_NAME, 'item')
    except:
        return
    try:
        browser.find_element(By.XPATH, '//*[@id="videoPlayer"]')
        watch_video(browser)
        return
    except:
        for i in range(len(videoList1)):
            try:
                # video = browser.find_element(By.XPATH, '''/html/body/div[4]/div[2]'''
                #                  ).find_elements(By.CLASS_NAME, 'item')[i]
                video = browser.find_elements(By.XPATH, '''/html/body/div[4]/div[2]/div/a/div''')[i]
            except:
                continue
            try:
                video.click()
            except:
                continue
            sleep(1)
            loop_floor(browser)
            browser.back()
            sleep(1)


def main():
    # 1.创建Chrome浏览器对象，这会在电脑上在打开一个浏览器窗口
    chrome_driver_path = r"E:\pythonProject\autoclass\venv\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe"
    browser = webdriver.Chrome(executable_path=chrome_driver_path)

    url = r"https://jste.net.cn/uids/"

    # 2.通过浏览器向服务器发送URL请求
    browser.get(url)
    # browser.get("https://www.baidu.com/")

    sleep(1)

    # 3.刷新浏览器
    browser.refresh()

    # 4.设置浏览器的大小
    # browser.set_window_size(1400, 800)
    browser.maximize_window()

    # 5.用户登录
    username_ = "xxx"  # stands for !@user
    password_ = "xxxxxxx"

    # 进入账户密码输入页面,找到用户密码框，填写内容
    user = browser.find_elements(By.XPATH, '//*[@id="loginName"]')[0]
    user.send_keys(username_)
    sleep(1)
    password = browser.find_elements(By.XPATH, '//*[@id="pwd"]')[0]
    password.send_keys(password_)
    sleep(1)

    # 输入验证码
    input_imgcode = browser.find_element(By.XPATH, '''//*[@id="randomCode"]''')
    input_imgcode.send_keys("") # 将光标定位到输入框，刷新验证码
    
    # TODO 每十秒判断一次验证码是否输入完成
    # while True:
    #     start = browser.find_element(By.XPATH, '''//*[@id="train_now"]/ul/li[4]/a''')
    #     if start.text == '开始学习':
    #         break
    #     sleep(10)
    sleep(10)

    # 登录
    submit = browser.find_element(By.XPATH, "/html/body/table[1]/tbody/tr[4]/td/form/input[4]")
    submit.click()
    sleep(1)

    # 点击开始学习
    browser.switch_to.frame('mainFrame')  # 切换frame
    start = browser.find_element(By.XPATH, '''/html/body/div[2]/div[2]/div/div[2]/ul/li[4]/a''')
    start.click()
    sleep(1)
    # 切换新window
    browser.switch_to.window(browser.window_handles[1])
    sleep(1)
    # 点击好的
    ok = browser.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div/div[2]/a[1]')
    ok.click()
    sleep(1)
    # 进入根目录
    root = browser.find_element(By.XPATH, '''/html/body/div[1]/div/ol/li[1]/a''')
    root.click()
    sleep(1)

    loop_floor(browser)

    # browser.close()


if __name__ == "__main__":
    main()
