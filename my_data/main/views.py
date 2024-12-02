from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# @login_required
def render_home_page(request):
    # file = get_object_or_404(File, file_id=1)
    # csv_data = None
    
    # try:
    #     csv_data = pd.read_csv(file.path, delimiter=';')
    # except Exception as e:
    #     print(f"Ошибка чтения файла! {e}")

    return render(request, 'main/home_page.html')
