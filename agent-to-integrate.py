from browser_use import Agent, Browser, ChatAnthropic
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()


async def main():
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

    task2= """Go to https://www.kijiji.ca/p-select-category.html. Click Alberta and then click Red Deer. Clock Go. Go to post ad button again:
    - Click x on the middle right to close the popup
    - Title (text input): sample product
    - Category Buy and Sell
    - Select Books
    - Select Textbooks
    - Select Im offering for ad type
    - Select for sale by owner
    - Description (text input): sample description here
    - DO NOT CLICK SELECT IMAGES
    - Enter the price (input field): '13'
    - CLICK POST YOUR AD BUTTON
    """

    agent.add_new_task(task2)
    
    await agent.run()

    await browser.kill()


if __name__ == "__main__":
    asyncio.run(main())
