# mwsgeneric-base-html parbase section
from langchain.document_loaders import ReadTheDocsLoader
from typing import List, Dict
from langchain.docstore.document import Document
from pathlib import Path
import logging
import pdb, os
import chardet


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ExtendReadTheDocsLoader(ReadTheDocsLoader):
    def load(
        self, mainContentTagKey: str = None, mainContentTagDict: Dict = None
    ) -> List[Document]:
        """Load documents."""
        from bs4 import BeautifulSoup

        def _find_encoding_in_html(filePath: str):
            # Open the file in binary mode
            with open(filePath, "rb") as f:
                # Read the first few bytes of the file
                data = f.read()
                # detect the encoding
                result = chardet.detect(data)
                encoding = result["encoding"]

            return encoding

        def _clean_data(data: str) -> str:
            soup = BeautifulSoup(data, **self.bs_kwargs)
            text = []
            if len(text) == 0:
                text = soup.find_all("main", {"id": "main-content"})
                print(f"Using main, id, main-content")
                print(f">> text length: {len(text)}")

            if len(text) == 0:
                text = soup.find_all("main", {"property": "mainContentOfPage"})
                print(f"Using main, property, mainContentOfPage")
                print(f">> text length: {len(text)}")

            if len(text) == 0:
                print(f"Using div, role, main")
                text = soup.find_all("div", {"role": "main"})
                print(f">> text length: {len(text)}")

            if (
                mainContentTagDict is not None
                and mainContentTagKey is not None
                and len(text) == 0
            ):
                print(f"Using {mainContentTagKey}, {mainContentTagDict}")
                text = soup.find_all(mainContentTagKey, mainContentTagDict)
                print(f">> text length: {len(text)}")

            if len(text) != 0:
                text = text[0].get_text().strip()
                print(f"Text: {text[:100]}")
            else:
                text = ""
                print(f"There is NO text for this!!!!")
            return "\n".join([t for t in text.split("\n") if t])

        docs = []
        # TODO: remove count
        totalFiles = 0
        counts = [0, 0, 0]
        for p in Path(self.file_path).rglob("*"):
            if p.is_dir():
                continue
            totalFiles += 1
            print(f"======================================")
            # Find encoding
            encoding = _find_encoding_in_html(p)
            try:
                with open(p, "r", encoding=encoding) as f:
                    print(f"----------\nProceed {p} using {encoding}")
                    text = _clean_data(f.read())
                    counts[0] += 1
            except:
                with open(p, "r", encoding="Windows-1252") as f:
                    print(f"----------\nProceed {p} using Windows-1252")
                    text = _clean_data(f.read())
                    counts[1] += 1
            finally:
                try:
                    with open(p, "r", encoding=self.encoding) as f:
                        print(f"----------\nProceed {p} using {self.encoding}")
                        text = _clean_data(f.read())
                        counts[2] += 1
                except UnicodeDecodeError as e:
                    print(f"[Error] {e} when trying to open {p}! SKip this file!")
                    continue
            # TODO: remove
            # dump data to a txt file for logs
            logFileName = p.name
            with open(f".logs/{logFileName}.txt", "w") as logFile:
                print(f"Write log .logs/{logFileName}")
                logFile.write(str(p))
                logFile.write("\n")
                logFile.write("======================")
                logFile.write("\n")
                logFile.write(text)

            metadata = {"source": str(p)}
            docs.append(Document(page_content=text, metadata=metadata))

            # TODO: remove
            print(
                f"Sofar, proceeded using encoding-finding: {counts[0]} |using Window encoding: {counts[1]} |using {self.encoding}: {counts[2]}"
            )

            # TODO: remove
            if sum(counts) == 1000:
                break
        print(f"==================================================")
        print(f"TOTAL files: {totalFiles}")
        print(
            f"TOTAL Proceeding using encoding-finding: {counts[0]} |using Window encoding: {counts[1]} |using {self.encoding}: {counts[2]}"
        )

        return docs
