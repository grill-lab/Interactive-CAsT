from abc import ABC, abstractmethod

class AbstractIndexGenerator(ABC):

    @abstractmethod
    def generate_index(self, input_directory, output_directory) -> None:
        """
        Generates an index for use within the online system.
        """
        pass