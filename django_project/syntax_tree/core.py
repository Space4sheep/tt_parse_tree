from abc import ABC, abstractmethod

from typing import Iterator, List, Dict, Any

from nltk import ParentedTree, Tree


class SyntaxTreeStorage(ABC):
    @classmethod
    @abstractmethod
    def from_string(cls, tree: str) -> 'SyntaxTreeStorage':
        """
        Abstract method for creating a tree from a string.
        """
        pass


class SyntaxTreeProcessor(ABC):
    storage_class = SyntaxTreeStorage

    def __init__(self, tree: str):
        self.tree_storage = self.storage_class.from_string(tree)

    @abstractmethod
    def create_trees(self) -> Iterator[Any]:
        """
        Method for creating trees using different methods for paraphrasing.
        """
        pass

    @abstractmethod
    def find_np(self) -> List[Dict[str:Any, str:tuple]]:
        """
        Method for finding NP nodes that meet the requirements.
        """
        pass

    @abstractmethod
    def build_paraphrases(self) -> Dict:
        pass
