from django.http import JsonResponse

from syntax_tree.np_paraphrase_generator import NLTKProcessor


def paraphrase(request):

    tree_str = request.GET.get('tree', '')

    result = NLTKProcessor(tree_str).build_paraphrases()

    return JsonResponse(result)
