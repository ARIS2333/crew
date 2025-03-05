import streamlit as st
import tempfile
import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

# Streamlit 页面配置
st.set_page_config(
    page_title="自动化提交系统",
    page_icon="🤖",
    layout="wide"
)
st.title("自动化提交系统")

# 侧边栏配置：登录信息和其他设置
st.sidebar.header("登录设置")
username = st.sidebar.text_input("用户名", value="371302200702171235")
password = st.sidebar.text_input("密码", type="password", value="Zyx1234567")
headless = st.sidebar.checkbox("启用无头模式", value=False)
file_path = st.sidebar.text_input("佐证材料文件路径", value="/Users/alice/CODE_Projects/web/error.png")

if st.button("开始自动化提交"):
    with st.spinner("正在运行自动化提交..."):
        driver = None  # 初始化driver变量
        temp_dir = tempfile.mkdtemp()  # 创建临时目录
        try:
            st.write("创建临时Chrome用户数据目录:", temp_dir)
            
            chrome_options = Options()
            # 添加必要的Chrome选项
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            if headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument(f"--user-data-dir={temp_dir}")
            # 可选：随机调试端口
            chrome_options.add_argument(f"--remote-debugging-port={random.randint(1000, 9999)}")
            
            st.write("正在初始化 WebDriver...")
            driver = webdriver.Chrome(options=chrome_options)
            driver.maximize_window()

            # ---------------登录流程---------------
            st.write("正在登录...")
            driver.get("https://szpj.sdei.edu.cn/zhszpj/uc/login.htm")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "j_username"))
            ).send_keys(username)
            driver.find_element(By.ID, "j_password").send_keys(password)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "loginBtn"))
            ).click()
            st.write("登录成功!")
            
            # 关闭新手指引
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, "jpwClose"))
            ).click()
            
            # ---------------打开典型事例页面---------------
            driver.get("https://szpj.sdei.edu.cn/zhszpj/web/sxpd/xsDxsl.htm")
            
            # 等待并点击“添加”按钮
            add_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-add"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
            time.sleep(0.5)
            ActionChains(driver).move_to_element(add_button).click().perform()
            st.write("成功点击添加按钮！")
            
            # ---------------填写典型事例信息---------------
            
            # 典型事例-活动主题
            THEME = "测试活动主题"
            theme_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "dxslHdzt"))
            )
            theme_input.click()
            theme_input.clear()
            theme_input.send_keys(THEME)
            
            # 典型事例-活动类型
            TYPE = "社团活动"
            select_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "dxslHdlx"))
            )
            select = Select(select_element)
            select.select_by_visible_text(TYPE)
            
            # 典型事例-活动时间
            START_TIME = "2023-10-01"
            END_TIME = "2023-10-02"
            starttime_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "dxslKssj"))
            )
            driver.execute_script("arguments[0].removeAttribute('readonly')", starttime_input)
            starttime_input.clear()
            starttime_input.send_keys(START_TIME)
            
            endtime_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "dxslJssj"))
            )
            driver.execute_script("arguments[0].removeAttribute('readonly')", endtime_input)
            endtime_input.clear()
            endtime_input.send_keys(END_TIME)
            
            # 典型事例-活动地点
            LOCATION = "测试活动地点"
            location_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "dxslHddd"))
            )
            location_input.clear()
            location_input.send_keys(LOCATION)
            
            # 典型事例-典型事例描述
            DESCRIPTION = ("学习新思想，争做新青年，青年大学习。国家尚未富强，怎谈儿女情长，"
                           "欣逢盛世，当不负盛世。愿中华儿女自立自强。青春逢盛世，奋斗正当时，"
                           "我们要向着红旗指引的方向，以于笃定前行，以奋斗开启未来!")
            desc_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "dxslDxslms"))
            )
            desc_element.clear()
            desc_element.click()
            desc_element.send_keys(DESCRIPTION)
            
            # 典型事例-佐证材料类型
            MATERIAL_TYPE = "文件"
            select_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "zzcllx"))
            )
            select = Select(select_element)
            select.select_by_visible_text(MATERIAL_TYPE)
            
            # 典型事例-佐证材料上传
            file_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "file"))
            )
            file_input.send_keys(file_path)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "saveFile"))
            ).click()
            
            # 典型事例-保存
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "saveDxsl"))
            ).click()
            ok_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm"))
            )
            ok_button.click()
            st.success("自动化提交成功！")
        except Exception as e:
            st.error(f"自动化执行失败: {e}")
        finally:
            if driver is not None:
                driver.quit()
                st.write("WebDriver已关闭。")
                # 可选：清理临时目录
                # import shutil
                # shutil.rmtree(temp_dir, ignore_errors=True)