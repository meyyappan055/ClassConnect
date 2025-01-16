import sys
import os
import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time



def navigate_batch1(page):
    page.get_by_role("link", name=" Unified Time Table").click()
    page.get_by_role("link", name=" Unified Time Table 2024-Batch").click()
    # time.sleep(3)


def navigate_batch2(page):
    page.get_by_role("link", name=" Unified Time Table", exact=True).click()
    page.get_by_role("link", name=" Unified Time Table-2024-Batch").click()
    # time.sleep(3)


def scrape_batch1_data(page):
    page.reload()
    page.wait_for_load_state('domcontentloaded')
    page.wait_for_selector("table", timeout=4000)
    page_html = page.content()
    soup = BeautifulSoup(page_html, "html.parser")
    table = soup.find("table", {"align": "center"})
    rows = table.find_all("tr")
    
    batch1_data = []
    for row in rows:
        columns = row.find_all("td")
        column_data = [column.text.strip() for column in columns]
        batch1_data.append(column_data)

    return batch1_data


def scrape_batch2_data(page):
    # page.reload()
    # page.wait_for_load_state('domcontentloaded')
    # page.wait_for_selector("table", timeout=4000)
    page_html = page.content()
    soup = BeautifulSoup(page_html, "html.parser")
    table = soup.find("table", {"align": "center"})
    rows = table.find_all("tr")
    
    batch2_data = []
    for row in rows:
        columns = row.find_all("td")
        column_data = [column.text.strip() for column in columns]
        batch2_data.append(column_data)

    return batch2_data

