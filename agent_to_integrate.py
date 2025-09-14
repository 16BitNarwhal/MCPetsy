from browser_use import Agent, Browser, ChatAnthropic
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

async def main(product_info=None):
    llm = ChatAnthropic(model="claude-sonnet-4-0", temperature=0.0)

    browser = Browser(
        headless=False,
        window_size={"width": 1000, "height": 700},
        keep_alive=True
    )

    await browser.start()

    task = f"""Go to kijiji.ca and sign in with these credentials (in 2 separate text fields):
    - Username: {os.getenv("KIJIJI_USERNAME")}
    - Password: {os.getenv("KIJIJI_PASSWORD")}
    
    Navigate to the login page, enter the credentials, and complete the sign-in process."""

    agent = Agent(
        task=task,
        browser_session=browser,
        llm=llm,
    )

    await agent.run()

    if product_info:
        title = product_info.get("title", "sample product")
        description = product_info.get("description", "sample description here")
        price = product_info.get("price", "13")
        category = product_info.get("category", "Books")
    else:
        title = "sample product"
        description = "sample description here"
        price = "13"
        category = "Books"

    task2 = f"""Go to https://www.kijiji.ca/p-select-category.html. Click Alberta and then click Red Deer. Click Go. Go to post ad button again:
    - Click x on the middle right to close the popup
    - Title (text input): {title}
    - Category Buy and Sell
    - Select a category that is {category}
    - If you are on a subcategory page, select a random subcategory
    - Select Im offering for ad type
    - Select for sale by owner
    - Description (text input): {description}
    - DO NOT CLICK SELECT IMAGES
    - Enter the price (input field): '{price}'
    - Click the Post Your Ad button at the bottom of the page to finish the process
    """

    agent.add_new_task(task2)
    
    await agent.run()

    task3 = f'''Check only my most recent (first) conversation on Kijiji. You are acting as a seller for my item and your goal is to sell the item to the interested buyer.
    You should not need to scroll the page at all.
    Only send a message if the interested buyer has started the conversation or responded to my last message, otherwise wait for a response. 
    To end the conversation, discuss a location and time to meetup with the buyer.
    While waiting, return to the Messages List page and click back into the most recent (first) conversation to check for new messages.
    The price of the item is {price}. If the buyer tries to offer a lower price, you should negotiate and counteroffer a price somewhere between the price and the buyer's offer.
    Ensure you correctly click the sendButton after drafting the message.
    '''

    agent.add_new_task(task3)

    await agent.run()

    await browser.kill()

if __name__ == "__main__":
    asyncio.run(main())
