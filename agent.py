from browser_use import Agent, Browser, ChatAnthropic
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

async def main():
    llm = ChatAnthropic(model='claude-3-5-haiku-latest', temperature=0.0)
    
    browser = Browser(
        headless=False,
        window_size={'width': 1000, 'height': 700},
    )
    
    task = f'''Go to kijiji.ca and sign in with these credentials:
    - Username: {os.getenv('KIJIJI_USERNAME')}
    - Password: {os.getenv('KIJIJI_PASSWORD')}
    
    Navigate to the login page, enter the credentials, and complete the sign-in process."""
    
    agent = Agent(
        task=task,
        browser=browser,
        llm=llm,
    )
    
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())