from .abstract_index_generator import AbstractIndexGenerator
import subprocess

class PyseriniIndexGenerator(AbstractIndexGenerator):

    def generate_index(self, input_directory, output_directory) -> None:

        subprocess.run(["python3", "-m", "pyserini.index",
                        "-collection", "TrecwebCollection",
                        "-generator", "DefaultLuceneDocumentGenerator",
                        "-threads", "8",
                        "-input", input_directory,
                        "-index", output_directory,
                        "-storePositions", "-storeRaw", "-storeDocvectors"])
