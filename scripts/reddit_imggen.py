from playwright.sync_api import sync_playwright
import os

def generate_reddit_post(story):
    # Load HTML and insert dynamic story
    with open("templates/reddit_template.html", "r", encoding="utf-8") as file:
        html_template = file.read()

    html_filled = html_template.replace("[STORY_TEXT]", story)

    # Save temp file
    with open("templates/reddit_render.html", "w", encoding="utf-8") as f:
        f.write(html_filled)

    # Screenshot using Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("file://" + os.path.abspath("templates/reddit_render.html"))
        element = page.locator(".card")
        element.screenshot(path="static/reddit_post.png", omit_background=True)
        browser.close()
