from django.http import JsonResponse

from syntax_tree.np_paraphrase_generator import NLTKProcessor


def paraphrase(request):

    tree_str = request.GET.get('tree', '')
    # The number of generated paraphrases. The default is -20.
    limit = int(request.GET.get('limit', '20'))

    result = NLTKProcessor(tree_str).build_paraphrases(limit)

    return JsonResponse(result)
