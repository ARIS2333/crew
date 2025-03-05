import streamlit as st
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import datetime

# 页面配置
st.set_page_config(
    page_title="教育平台自动化助手",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)

# CSS样式美化
st.markdown("""
<style>
div[data-baseweb="select"] > div {
    border-radius: 8px;
}
button {
    background: #4CAF50 !important;
    color: white !important;
}
.stDateInput > div > input {
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

def run_automation(config):
    """执行自动化任务的函数"""
    try:
        # --------------- 初始化浏览器 ---------------

        headless = False
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()

        # --------------- 登录流程 ---------------
        driver.get("https://szpj.sdei.edu.cn/zhszpj/uc/login.htm")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "j_username"))
        ).send_keys(config['username'])
        driver.find_element(By.ID, "j_password").send_keys(config['password'])
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "loginBtn"))
        ).click()
        print("登录成功!")
        
        # --------------- 导航到目标页面 ---------------
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "jpwClose"))
        ).click()
        print("关闭新手指引！")
        driver.get("https://szpj.sdei.edu.cn/zhszpj/web/sxpd/xsDxsl.htm")

        # --------------- 填写表单 ---------------
        # 点击添加按钮
        add_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-add"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
        ActionChains(driver).move_to_element(add_button).click().perform()
        print("成功点击添加按钮！")
        # 填写活动信息
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dxslHdzt"))
        ).send_keys(config['theme'])
        print("填写活动主题！")
        # 选择活动类型
        Select(WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dxslHdlx"))
        )).select_by_visible_text(config['activity_type'])

        # 设置时间（处理日期输入）
        for elem_id, date in [("dxslKssj", config['start_date']), ("dxslJssj", config['end_date'])]:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, elem_id)))
            driver.execute_script(f"arguments[0].value = '{date}';", element)

        # 填写地点和描述
        driver.find_element(By.ID, "dxslHddd").send_keys(config['location'])
        desc_element = driver.find_element(By.ID, "dxslDxslms")
        driver.execute_script(f"arguments[0].value = '{config['description']}';", desc_element)

        # 文件上传
        if config['upload_file'] is not None:
            file_path = os.path.join(os.getcwd(), config['upload_file'].name)
            with open(file_path, "wb") as f:
                f.write(config['upload_file'].getbuffer())
            
            driver.find_element(By.ID, "file").send_keys(file_path)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "saveFile"))
            ).click()

        # 保存并确认
        driver.find_element(By.ID, "saveDxsl").click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm"))
        ).click()

        driver.quit()
        return True
    except Exception as e:
        st.error(f"自动化执行失败: {str(e)}")
        return False

# 侧边栏 - 登录凭证
with st.sidebar:
    st.header("🔐 登录设置")
    config = {
        'username': st.text_input("用户名", value='371302200702171235'),
        'password': st.text_input("密码", type="password", value="Zyx1234567"),
        'browser': st.selectbox("选择浏览器", ['Safari', 'Chrome'])
    }

# 主界面
st.title("🎯 典型事例提交系统")
st.markdown("---")

with st.form("main_form"):
    # 第一列 - 基本信息
    col1, col2 = st.columns(2)
    with col1:
        config['theme'] = st.text_input("活动主题", value="测试活动主题")
        config['activity_type'] = st.selectbox("活动类型", ["社团活动", "志愿活动", "学术活动"])
        
    with col2:
        config['start_date'] = st.date_input("开始日期", value=datetime.date(2023, 10, 1)).strftime("%Y-%m-%d")
        config['end_date'] = st.date_input("结束日期", value=datetime.date(2023, 10, 2)).strftime("%Y-%m-%d")

    
    # 第二列 - 详细信息
    col3, col4 = st.columns(2)
    with col3:
        config['location'] = st.text_input("活动地点", value="测试活动地点")
    with col4:
        config['upload_file'] = st.file_uploader("佐证材料", type=['png', 'jpg', 'pdf'])

    # 描述信息
    config['description'] = st.text_area(
        "事例描述", 
        value="测试典型事例描述...",
        height=150
    )

    # 提交按钮
    if st.form_submit_button("🚀 开始自动化提交", use_container_width=True):
        with st.spinner("正在自动化提交，请稍候..."):
            if run_automation(config):
                st.success("提交成功！")
                st.balloons()