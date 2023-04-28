from itertools import permutations
from typing import Dict, List, Iterator

from nltk.tree import Tree
from nltk.tree import ParentedTree


def find_np(tree: ParentedTree) -> List[Dict[str:ParentedTree, str:tuple]]:
    """
    Function to search for all noun phrases separated by a comma or a connecting phrase in a tree
    """
    # Use a list, not an iterator, to check for duplicates
    result = []

    # We find the nodes we need
    for subtree in tree.subtrees(lambda t: t.label() == 'NP'):
        left_sibling = subtree.left_sibling()
        right_sibling = subtree.right_sibling()

        # Find pairs that are separated by a comma or a conjunction phrase
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


def create_new_subtrees(subtree: ParentedTree) -> Iterator[ParentedTree]:
    """
    Function for generating new subtrees using the permutation method np between which there is a comma or a conjunction
    """
    # Find all NPs inside the subtree
    nps = [node for node in subtree if node.label() == 'NP']
    # Generate possible NPS combinations
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


def create_new_trees(tree: str) -> Iterator[ParentedTree]:
    """
    Function that generates all possible variations of a tree
    using the NP permutation method with a comma or a ligature between them.
    """
    # Convert string to an object of type ParentTree.
    ptree = ParentedTree.fromstring(tree)
    # Get a list of suitable NPs to change and their position in the tree.
    nps = find_np(ptree)

    # Create a new tree for each NP that has been changed.
    for np in nps:
        for new_subtree in list(create_new_subtrees(np['subtree'])):
            new_subtree = ParentedTree.convert(new_subtree)
            new_tree = ptree.copy(deep=True)
            new_tree[np['position']] = new_subtree
            yield new_tree
