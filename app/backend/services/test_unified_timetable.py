import sys
import os
import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

def navigate_batch1(page):
    page.get_by_role("link", name="Unified Time Table", exact=True).click()
    page.wait_for_load_state("networkidle")
    page.get_by_role("link", name="Unified Time Table 2024-Batch").click()
    time.sleep(2)
    page.wait_for_load_state("networkidle")

def navigate_batch2(page):
    page.get_by_role("link", name="Unified Time Table", exact=True).click()
    page.wait_for_load_state("networkidle")
    page.get_by_role("link", name="Unified Time Table-2024-Batch").click()
    time.sleep(2)
    page.wait_for_load_state("networkidle")


def scrape_batch1_data(page):
    try:
        page.wait_for_load_state('domcontentloaded')
        page.wait_for_selector("table[align='center']", timeout=10000) 

        page_html = page.content()
        soup = BeautifulSoup(page_html, "html.parser")

        table = soup.find("table", {"align": "center"})
        if not table:
            raise Exception("Table not found after navigation")
            
        rows = table.find_all("tr")
        
        batch1_data = []
        for row in rows:
            columns = row.find_all("td")
            column_data = [column.text.strip() for column in columns]
            batch1_data.append(column_data)
        
        print(f"Successfully scraped {len(batch1_data)} rows")
        return batch1_data
        
    except Exception as e:
        print(f"Error in scrape_batch1_data: {str(e)}")
        raise

def scrape_batch2_data(page):
    try:
        page.wait_for_load_state('domcontentloaded')
        page.wait_for_selector("table[align='center']", timeout=10000)

        page_html = page.content()
        soup = BeautifulSoup(page_html, "html.parser")

        table = soup.find("table", {"align": "center"})
        if not table:
            raise Exception("Table not found after navigation")

        rows = table.find_all("tr")
        
        batch2_data = []
        for row in rows:
            columns = row.find_all("td")
            column_data = [column.text.strip() for column in columns]
            batch2_data.append(column_data)
        
        print(f"Successfully scraped {len(batch2_data)} rows")
        return batch2_data
        
    except Exception as e:
        print(f"Error in scrape_batch2_data: {str(e)}")
        raise