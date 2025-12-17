import asyncio

# Captures the screenshot from your local computer
from oagi import AsyncScreenshotMaker 

# Controls your local keyboard and mouse based on the model predicted actions
from oagi import AsyncPyautoguiActionHandler 
from oagi import TaskerAgent

async def main():
    agent = TaskerAgent(model="lux-actor-1")

    agent.set_task(
        task="Use chase to calculate mortgage payments",
        todos=[
            "Go to https://www.chase.com/personal/mortgage/calculators-resources/mortgage-calculator",
            "Scroll down to 'Customize your info' and change the Credit score to 'Very good (700-739)'",
            "Set the 'Property use' to 'Investment property' and set 'Property type' to 'Condo' ",
            "For the County type 'San Francisco' and select CA, San Francisco from the autocomplete dropdown",
            "Set the property price to 2000000, the down payment to '400000', and click 'Loan Options'",
        ]
    )

    await agent.execute(
        instruction="Use chase to calculate mortgage payments",
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )

asyncio.run(main())