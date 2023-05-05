import time, os
import asyncio
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import pdb

load_dotenv()


async def test_async_chat_LLM():
    llm = ChatOpenAI(temperature=0, streaming=True)
    systemMessage = SystemMessage(
        content="You are a lawyer. Answer every question using bullet points and markdown format."
    )
    userMessage = HumanMessage(content="Hello. How are you?")
    answer = await llm.agenerate(messages=[[userMessage, systemMessage]])
    print(f"[ChatOpenAI] Question: Hello. How are you?")
    print(f"[ChatOpenAI] Response: {answer.generations[0][0].text.strip()}")

    question = "How many islands Vietnam has?"
    userMessage = HumanMessage(content=question)
    print(f"[ChatOpenAI] Question: {question}")
    answer = await llm.agenerate(messages=[[userMessage]])
    print(f"[ChatOpenAI] Response: {answer.generations[0][0].text.strip()}")

    question = "Which one is the largest?"
    userMessage = HumanMessage(content=question)
    print(f"[ChatOpenAI] Question: {question}")
    answer = await llm.agenerate(messages=[[userMessage]])
    print(f"[ChatOpenAI] Response: {answer.generations[0][0].text.strip()}")

    question = "Write 300 words about the largest island in vietnam"
    userMessage = HumanMessage(content=question)
    print(f"[ChatOpenAI] Question: {question}")
    answer = await llm.agenerate(messages=[[userMessage]])
    print(f"[ChatOpenAI] Response: {answer.generations[0][0].text.strip()}")


async def test_simple_async_LLM():
    import openai

    openai.api_key = os.environ[
        "OPENAI_API_KEY"
    ]  # supply your API key however you choose
    completion_resp = await openai.Completion.acreate(
        prompt="This is a test", model="davinci"
    )
    print(f"========================================")
    print(f"===> Async completion resp: {completion_resp}")
    print(f"========================================")


def generate_serially():
    llm = OpenAI(temperature=0.9)  # , openai_api_key=OPENAI_API_KEY)
    for _ in range(2):
        resp = llm.generate(["Hello, how are you?"])
        print(f"[sequential]{resp.generations[0][0].text.strip()}")


async def async_generate(llm):
    resp = await llm.agenerate(["Hello, how are you?"])
    print(f"[async]{resp.generations[0][0].text.strip()}")


async def generate_concurrently():
    llm = OpenAI(temperature=0.9, verbose=True)
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
    # os.environ["SSL_CERT_FILE"] = "/etc/ssl/certs/ca-certificates.crt"
    # create an event loop
    loop = asyncio.get_event_loop()

    # run the main function
    # loop.run_until_complete(main())
    # loop.run_until_complete(test_simple_async_LLM())
    loop.run_until_complete(test_async_chat_LLM())
