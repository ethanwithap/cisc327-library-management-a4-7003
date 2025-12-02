from playwright.sync_api import sync_playwright
import uuid
import random

BASE_URL = "http://localhost:5000"




def start_browser():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    return p, browser, page


def stop_browser(p, browser):
    browser.close()
    p.stop()




def _generate_unique_isbn() -> str:
    digits = "".join(str(random.randint(0, 9)) for _ in range(10))
    return "978" + digits



def test_add_book_and_verify_catalog():
    """
    Flow 1:
    1. Open home page
    2. select add book
    3. submits new valid book
    4. check catalog for update
    """

    unique_title = f"PlaywrightBook-{uuid.uuid4().hex[:6]}"
    isbn = _generate_unique_isbn()

    p, browser, page = start_browser()

    try:
        
        page.goto(BASE_URL)

        
        page.get_by_text("Add Book").click()

       
        page.fill('input[name="title"]', unique_title)
        page.fill('input[name="author"]', "Author Test")
        page.fill('input[name="isbn"]', isbn)
        page.fill('input[name="total_copies"]', "3")

        
        page.get_by_role("button", name="add book to catalog").click()
        page.wait_for_timeout(600)

       
        page.goto(f"{BASE_URL}/catalog")
        page.wait_for_timeout(400)
        content = page.content()
        assert unique_title in content

    finally:
        stop_browser(p, browser)




def test_view_catalog_shows_sample_books():
    """
    flow 2:
    1. Go to catalog
    2. check if data from add book appears
    """

   
    sample_titles = [
        "The Great Gatsby",
        "To Kill a Mockingbird",
        "1984",
    ]

    p, browser, page = start_browser()

    try:
      
        page.goto(f"{BASE_URL}/catalog")
        page.wait_for_timeout(400)

        content = page.content()

        
        for title in sample_titles:
            assert title in content, f"Expected '{title}' to be in the catalog page."

    finally:
        stop_browser(p, browser)
