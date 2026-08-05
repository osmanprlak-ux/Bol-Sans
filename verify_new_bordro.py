import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        filepath = f"file://{os.path.abspath('index.html')}"
        await page.goto(filepath)

        # Test Case: Brüt'ten Net'e (SGK Muaf, Özel Kesinti, Günlük Kırılım)
        await page.select_option('#calcType', 'brut2net')
        await page.fill('#baseSalary', '40000') # 40 bin brüt
        await page.fill('#holidayDays', '4') # 4 gün tatil çalışması
        await page.fill('#overtimeHours', '10') # 10 saat mesai

        # Ek ödemeler doldurma (Ayni Yardım ve SGK Muaf)
        desc_inputs = await page.locator('.add-pay-desc').all()
        amount_inputs = await page.locator('.add-pay-amount').all()
        type_inputs = await page.locator('.add-pay-type').all()

        await desc_inputs[0].fill('Alışveriş Kartı')
        await amount_inputs[0].fill('5000')
        await type_inputs[0].select_option('in_kind') # Ayni yardım

        await desc_inputs[1].fill('Yol Yardımı')
        await amount_inputs[1].fill('1500')
        await type_inputs[1].select_option('normal')

        # Özel Kesinti doldurma
        spec_desc_inputs = await page.locator('.spec-ded-desc').all()
        spec_amount_inputs = await page.locator('.spec-ded-amount').all()

        await spec_desc_inputs[0].fill('BES Kesintisi')
        await spec_amount_inputs[0].fill('2000')

        # Hesapla
        await page.click('button[type="submit"]')

        # Animasyon beklemesi gerekmiyor ama render icin cok kisa bekleme
        await page.wait_for_timeout(1000)

        # Ekran görüntüsü al
        await page.screenshot(path='/home/jules/verification/new_bordro_brut2net.png', full_page=True)

        # Test Case 2: Netten Brüte kontrolü
        await page.select_option('#calcType', 'net2brut')
        await page.fill('#baseSalary', '30000') # Hedef net (kesinti öncesi)
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(1000)
        await page.screenshot(path='/home/jules/verification/new_bordro_net2brut.png', full_page=True)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
