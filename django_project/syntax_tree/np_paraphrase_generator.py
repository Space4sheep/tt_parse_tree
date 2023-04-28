from itertools import permutations
from typing import List, Dict, Iterator

from nltk import Tree, ParentedTree

from syntax_tree.core import SyntaxTreeProcessor, SyntaxTreeStorage


class NLTKStorage(SyntaxTreeStorage):
    """
    Syntax tree class that uses the functionality of the nltk library.
    """
    def __init__(self, tree: str):
        self.tree = Tree.fromstring(tree)
        self.ptree = ParentedTree.fromstring(tree)

    @classmethod
    def from_string(cls, tree: str) -> 'NLTKStorage':
        return cls(tree=tree)

    def p_convert(self, tree):
        return self.ptree.convert(tree)

    def subtrees(self, filter_func=None):
        return self.tree.subtrees(filter_func)

    def p_subtrees(self, filter_func=None):
        return self.ptree.subtrees(filter_func)


class NLTKProcessor(SyntaxTreeProcessor):
    storage_class = NLTKStorage

    def find_np(self) -> List[Dict[str:ParentedTree, str:tuple]]:
        """
        Method searches for NPs whose child nodes contain pairs of NPs with a comma or CC.
        Return a list of subtrees, with their positions in the tree
        """
        # Use a list, not an iterator, to check for duplicates
        result = []

        for subtree in self.tree_storage.p_subtrees(lambda t: t.label() == 'NP'):
            left_sibling = subtree.left_sibling()
            right_sibling = subtree.right_sibling()

            if (left_sibling is not None and
                left_sibling.label() in [',', 'CC'] and
                left_sibling.left_sibling().label() == 'NP') or \
                    (right_sibling is not None and
                     right_sibling.label() in [',', 'CC'] and
                     right_sibling.right_sibling().label() == 'NP'):

                # Save the subtree and its position if this subtree is not already in the list
                position = subtree.parent().treeposition()
                np_dict = {'subtree': subtree.parent(), 'position': position}
                if np_dict not in result:
                    result.append(np_dict)

        return result

    @staticmethod
    def create_subtrees(subtree: NLTKStorage) -> Iterator[NLTKStorage]:
        """
        Generate subtrees using the NP permutation method with a comma or CC between them.
        """
        # Find all child NPs from the resulting node.
        nps = [node for node in subtree if node.label() == 'NP']

        # Get all the possible combinations in the residual of the NP permutations.
        all_np_combo = permutations(nps)

        # Find all the commas and conjunctions, keep them to preserve the sentence structure
        commas_and_ccs = [node for node in subtree if node.label() == ',' or node.label() == 'CC']

        # Create new subtrees, as Tree object
        for combo in all_np_combo:
            new_subtree = []
            for i in range(len(combo)):
                new_subtree.append(combo[i])
                if i < len(commas_and_ccs):
                    new_subtree.append(commas_and_ccs[i])
            yield Tree('NP', new_subtree)

    def create_trees(self) -> Iterator[Tree]:
        """
        Generate new trees for each new subtree.
        """
        # Get a list of NPs that can be changed.
        nps = self.find_np()

        for np in nps:
            for subtree in list(self.create_subtrees(np['subtree'])):
                new_subtree = self.tree_storage.p_convert(subtree)
                new_tree = self.tree_storage.ptree.copy(deep=True)
                new_tree[np['position']] = new_subtree
                yield new_tree

    def build_paraphrases(self):
        trees = list(self.create_trees())

        for i, tree in enumerate(trees):
            trees[i] = {"tree": str(tree).replace('\n', '')}

        return {"paraphrases": trees}
