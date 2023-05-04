import time, os
import asyncio
from dotenv import load_dotenv
from langchain.llms import OpenAI

load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


def generate_serially():
    llm = OpenAI(temperature=0.9, openai_api_key=OPENAI_API_KEY)
    for _ in range(5):
        resp = llm.generate(["[sequential]Hello, how are you?"])
        print(f"[sequential]{resp.generations[0][0].text.strip()}")


async def async_generate(llm):
    resp = await llm.agenerate(["[async]Hello, how are you?"])
    print(f"[async]{resp.generations[0][0].text.strip()}")


async def generate_concurrently():
    llm = OpenAI(temperature=0.9, openai_api_key=OPENAI_API_KEY)
    tasks = [async_generate(llm) for _ in range(5)]
    await asyncio.gather(*tasks)


async def main():
    s = time.perf_counter()
    generate_serially()
    elapsed = time.perf_counter() - s
    print("\033[1m" + f"Serial executed in {elapsed:0.2f} seconds." + "\033[0m")

    s = time.perf_counter()
    # If running this outside of Jupyter, use asyncio.run(generate_concurrently())
    await generate_concurrently()
    elapsed = time.perf_counter() - s
    print("\033[1m" + f"Concurrent executed in {elapsed:0.2f} seconds." + "\033[0m")


if __name__ == "__main__":
    # create an event loop
    loop = asyncio.get_event_loop()

    # run the main function
    loop.run_until_complete(main())
