from itertools import permutations
from typing import Dict, List, Iterator

from nltk.tree import Tree
from nltk.tree import ParentedTree


def find_np(tree: ParentedTree) -> List[Dict[str:ParentedTree, str:tuple]]:
    """
    Функція для пошуку всіх noun phrase, розділених комою або зв'язковим зворотом, в дереві
    """

    result = []

    for subtree in tree.subtrees(lambda t: t.label() == 'NP'):
        left_sibling = subtree.left_sibling()
        right_sibling = subtree.right_sibling()

        if (left_sibling is not None and
            left_sibling.label() in [',', 'CC'] and
            left_sibling.left_sibling().label() == 'NP') or \
                (right_sibling is not None and
                 right_sibling.label() in [',', 'CC'] and
                 right_sibling.right_sibling().label() == 'NP'):

            position = subtree.parent().treeposition()
            np_dict = {'subtree': subtree.parent(), 'position': position}
            if np_dict not in result:
                result.append(np_dict)

    return result


def collect_np(np: ParentedTree) -> List[ParentedTree]:
    """
    Функція для збору всіх дочірніх noun phrase.
    """
    return [subtree for subtree in np if subtree.label() == 'NP']


def collect_comma_and_ccs(np: ParentedTree) -> List[tuple]:
    """
    Функція для збору всіх розділових знаків
    """
    return [subtree for subtree in np if subtree.label() == ',' or subtree.label() == 'CC']


def create_new_subtrees(subtree: ParentedTree) -> Iterator[ParentedTree]:
    # Отримуємо список всіх можливих комбінацій NP між собою
    all_np_combo = permutations(collect_np(subtree))

    commas = collect_comma_and_ccs(subtree)

    for combo in all_np_combo:
        new_subtree = []
        for i in range(len(combo)):
            new_subtree.append(combo[i])
            if i < len(commas):
                new_subtree.append(commas[i])
        new_subtree = Tree('NP', new_subtree)
        yield new_subtree


def create_new_trees(tree: ParentedTree) -> Iterator[ParentedTree]:
    """
    Функція, яка генерує всі можливі варіації дерева
    """
    nps = find_np(tree)
    for np in nps:
        for new_subtree in list(create_new_subtrees(np['subtree'])):
            new_subtree = ParentedTree.convert(new_subtree)
            new_tree = tree.copy(deep=True)
            new_tree[np['position']] = new_subtree
            yield new_tree
