"""Create a ChatVectorDBChain for question/answering."""
from langchain.callbacks.manager import AsyncCallbackManager
from langchain.callbacks.tracers import LangChainTracer
from langchain.chains import ChatVectorDBChain, ConversationalRetrievalChain
from langchain.chains.chat_vector_db.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.vectorstores.base import VectorStore
from dotenv import load_dotenv
import os, pdb

load_dotenv()
print(f"OPENAI KEY: {os.environ['OPENAI_API_KEY']}")


def get_chain(
    vectorstore: VectorStore, question_handler, stream_handler, tracing: bool = False
) -> ConversationalRetrievalChain:
    """Create a ChatVectorDBChain for question/answering."""
    # Construct a ChatVectorDBChain with a streaming llm for combine docs
    # and a separate, non-streaming llm for question generation
    manager = AsyncCallbackManager([])
    question_manager = AsyncCallbackManager([question_handler])
    stream_manager = AsyncCallbackManager([stream_handler])
    if tracing:
        tracer = LangChainTracer()
        tracer.load_default_session()
        manager.add_handler(tracer)
        question_manager.add_handler(tracer)
        stream_manager.add_handler(tracer)

    question_gen_llm = OpenAI(
        temperature=0,
        verbose=True,
        callback_manager=question_manager,
        openai_api_key=os.environ["OPENAI_API_KEY"],
    )
    streaming_llm = OpenAI(
        streaming=True,
        callback_manager=stream_manager,
        verbose=True,
        temperature=0,
        openai_api_key=os.environ["OPENAI_API_KEY"],
    )

    question_generator = LLMChain(
        llm=question_gen_llm, prompt=CONDENSE_QUESTION_PROMPT, callback_manager=manager
    )
    doc_chain = load_qa_chain(
        streaming_llm, chain_type="stuff", prompt=QA_PROMPT, callback_manager=manager
    )

    # # TODO: remove
    # result = question_generator.generate(
    #     [{"question": "tell a joke", "chat_history": []}]
    # )
    # pdb.set_trace()
    # result = doc_chain.acall({"question": "tell a joke", "chat_history": []})
    # pdb.set_trace()

    # TODO: uncomment
    # qa = ConversationalRetrievalChain.from_llm(
    #     question_gen_llm,
    #     retriever=vectorstore.as_retriever(),
    #     condense_question_prompt=CONDENSE_QUESTION_PROMPT,
    #     chain_type="stuff",
    #     verbose=False,
    #     combine_docs_chain_kwargs={
    #         "callback_manager": manager,
    #     },
    # )
    # return qa

    # TODO: remove
    qa = ConversationalRetrievalChain(  # <==CHANGE  ConversationalRetrievalChain instead of ChatVectorDBChain
        # vectorstore=vectorstore,             # <== REMOVE THIS
        retriever=vectorstore.as_retriever(),  # <== ADD THIS
        combine_docs_chain=doc_chain,
        question_generator=question_generator,
        callback_manager=manager,
    )
    return qa
