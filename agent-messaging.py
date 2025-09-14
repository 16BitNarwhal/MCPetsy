from browser_use import Agent

async def agent_messaging(agent: Agent, price: int):
    next_task = f'''Check only my most recent (first) conversation on Kijiji. You are acting as a seller for my item and your goal is to sell the item to the interested buyer.
You should not need to scroll the page at all.
Only send a message if the interested buyer has started the conversation or responded to my last message, otherwise wait for a response. 
To end the conversation, discuss a location and time to meetup with the buyer.
While waiting, return to the Messages List page and click back into the most recent (first) conversation to check for new messages.
The price of the item is {price}. If the buyer tries to offer a lower price, you should negotiate and counteroffer a price somewhere between the price and the buyer's offer.
Ensure you correctly click the sendButton after drafting the message.
'''
    agent.add_new_task(next_task)

    await agent.run()
