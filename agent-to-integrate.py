from browser_use import Agent, Browser, ChatAnthropic
from dotenv import load_dotenv
import asyncio
import os
from agent_messaging import agent_messaging

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
    - Select a category that is closest to {category}
    - If you are still on the same page, select an appropriate subcategory for {title}
    - Select Im offering for ad type
    - Select for sale by owner
    - Description (text input): {description}
    - DO NOT CLICK SELECT IMAGES
    - Enter the price (input field): '{price}'
    - CLICK POST YOUR AD BUTTON
    """

    agent.add_new_task(task2)
    
    await agent.run()

    await agent_messaging(agent, float(price))

    await browser.kill()

if __name__ == "__main__":
    asyncio.run(main())
