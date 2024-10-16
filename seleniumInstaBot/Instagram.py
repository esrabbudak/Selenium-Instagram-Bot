from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class Instagram:
    def __init__(self, email, password):
        self.browser = webdriver.Chrome()
        self.email = email
        self.password = password

    def signIn(self):
        self.browser.get("https://www.instagram.com/")
        
        
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id='loginForm']/div/div[1]/div/label/input"))).send_keys(self.email)
        
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id='loginForm']/div/div[2]/div/label/input"))).send_keys(self.password)

        
        self.browser.find_element(By.XPATH, "//*[@id='loginForm']/div/div[2]/div/label/input").send_keys(Keys.ENTER)

        time.sleep(5)

        
        try:
            not_now_button = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Şimdi Değil')]")))
            not_now_button.click()
        except:
            print("Bildirim penceresi açılmadı.")

        time.sleep(5)

    
    def getFollowers(self):
        self.browser.get("https://www.instagram.com/esrabbudakk")
        time.sleep(5)  

        try:
        
            followers_button = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/followers/')]"))
            )
            followers_button.click()
            time.sleep(5)  

            dialog = WebDriverWait(self.browser, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role=dialog]"))
            )
        except Exception as e:
            print(f"Takipçi penceresi açılırken bir hata oluştu: {e}")
            return

        usernames = set()
        last_height = self.browser.execute_script("return arguments[0].scrollHeight", dialog)
        scroll_attempts = 0

        while True:
            # JavaScript ile takipçi listesini kaydır
            self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
            time.sleep(2)  # Kaydırdıktan sonra bekle

            new_height = self.browser.execute_script("return arguments[0].scrollHeight", dialog)
            
            # Eğer yeni bir yükseklik varsa kaydırmaya devam et
            if new_height > last_height:
                last_height = new_height
                scroll_attempts = 0  # Yeni yükseklik olduğunda sıfırla
            else:
                scroll_attempts += 1
                if scroll_attempts > 5:  # 5 denemeden sonra hala yeni takipçi yoksa döngüden çık
                    print("Tüm takipçiler yüklendi, çıkılıyor.")
                    break

        # Takipçilerin isimlerini topla
        followers_div = dialog.find_elements(By.CSS_SELECTOR, "a[href*='/'] div div span")
        for user in followers_div:
            if user.text:
                usernames.add(user.text)

        if usernames:
            print("Kullanıcı İsimleri:")
            for username in usernames:
                print(username)

            with open("followers.txt", "w", encoding="utf-8") as f:
                for username in usernames:
                    f.write(f"{username}\n")
            print("Takipçi listesi 'followers.txt' dosyasına kaydedildi.")
        else:
            print("Takipçi bulunamadı.")




email = "kullanıcı adı"
password = "instagram şifresi"

instagram = Instagram(email, password)
instagram.signIn()
instagram.getFollowers()


