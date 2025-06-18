from dashboard.models import Child
from usuario.models import UsuarioChild
from django.shortcuts import get_object_or_404

def children_context(request):
    if not request.user.is_authenticated:
        return {}
    children_ids = UsuarioChild.objects.filter(user=request.user).values_list('child_id', flat=True)
    children = Child.objects.filter(id__in=children_ids)
    # Só altera selected_child se o usuário explicitamente passar child_id na query
    child_id = request.GET.get('child_id')
    if child_id and child_id.isdigit() and int(child_id) in children_ids:
        selected_child = get_object_or_404(Child, id=child_id)
        request.session['selected_child_id'] = int(child_id)
    else:
        # Mantém a seleção anterior do usuário, se houver
        selected_child_id = request.session.get('selected_child_id')
        if selected_child_id and selected_child_id in children_ids:
            selected_child = get_object_or_404(Child, id=selected_child_id)
        else:
            selected_child = children.first() if children else None
            if selected_child:
                request.session['selected_child_id'] = selected_child.id
    return {'children': children, 'selected_child': selected_child}
