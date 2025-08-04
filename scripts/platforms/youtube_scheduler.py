import re
from playwright.sync_api import Playwright, sync_playwright, expect
from openpyxl import load_workbook, Workbook
import datetime
import os
from scripts.excel import get_row_index

date = datetime.datetime.now().strftime("%b %d, %Y")
title = "Test Video"
video_path = "C:\\Users\\Kavin Seralathan\\Reddit-Story-Generator\\outputVideos\\output-1l2zkd0.mp4"
time = datetime.datetime.now().strftime("%I:%M %p")

excel_file = 'data/Reddit-Story-Generator.xlsx'
wb = load_workbook(excel_file)
ws = wb.active


def schedule_video(video_path, title, date, time):

    def run(playwright: Playwright) -> None:
        browser = playwright.chromium.launch_persistent_context(
            headless=False,
            user_data_dir="C:\\Users\\Kavin Seralathan\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            args=["--disable-blink-features=AutomationControlled"],
            )
        page = browser.new_page()
        page.goto("https://studio.youtube.com/channel/UCBwvgXbVAjN75fLy_g9e1tA")
        page.locator('ytcp-button#create-icon').click()
        page.get_by_text("Upload video").click()
        page.locator('input[type="file"]').set_input_files(video_path)
        page.get_by_role("textbox", name="Add a title that describes").fill(title)
        page.get_by_role("radio", name="No, it's not made for kids").click()
        page.get_by_label("Next", exact=True).click()
        page.get_by_label("Next", exact=True).click()
        page.get_by_label("Next", exact=True).click()
        page.get_by_role("button", name="Click to expand").click()
        page.locator("ytcp-dropdown-trigger").click()
        page.get_by_label("Enter date").get_by_label("").fill(date)
        page.locator("tp-yt-iron-overlay-backdrop").nth(2).click()
        page.locator("#input-1").get_by_label("").fill(time)
        #page.get_by_label("Schedule", exact=True).click()


        page.pause()


        # ---------------------
        browser.close()


    with sync_playwright() as playwright:
        run(playwright)

