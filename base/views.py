from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Dataset
# from .forms import DatasetForm
from .forms import DatasetFormFirstPage, DatasetFormSecondPage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pandas as pd
import csv
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
# Create your views here.


def give_recommendations(id):
  datasets = Dataset.objects.all()

  # Convert the Django QuerySet to a list of dictionaries
  data_dict = list(datasets.values())
  
  # Create a Pandas DataFrame from the list of dictionaries
  df = pd.DataFrame(data_dict)
  
  # Filling NaNs with empty string
  df["overview"] = df["overview"].fillna('')
  
  # Create a TFIDFVectorizer Object
  tfv = TfidfVectorizer(min_df=1, max_features=None, strip_accents="unicode", analyzer="word", token_pattern=r"\w{1,}", ngram_range=(1, 3), stop_words="english")
  
  # Fit the TfidfVectorizer on the "overview" text
  tfv_matrix = tfv.fit_transform(df["overview"])
  
  # Calculate the cosine similarity between all dataset
  cos_sim = cosine_similarity(tfv_matrix, tfv_matrix)

  id_to_index = {str(id_): index for index, id_ in enumerate(df["id"])}
  idx = id_to_index[str(id)]
  
  cos_sim_scores = list(enumerate(cos_sim[idx]))
  
  # Filter out datasets with a cosine similarity score of less than .00
  cos_sim_scores = [cos_sim_score for cos_sim_score in cos_sim_scores if cos_sim_score[1] > 0.00]
  cos_sim_scores = sorted(cos_sim_scores, key=lambda x: x[1], reverse=True)
  cos_sim_scores = cos_sim_scores[1:6]
  
  # Dataset indices
  dataset_indices = [cos_sim_score[0] for cos_sim_score in cos_sim_scores]
  similar_ids = [df.iloc[index]["id"] for index in dataset_indices]
  
  return similar_ids, cos_sim_scores

def home(request):
  q = request.GET.get('q', '') 
  datasets = Dataset.objects.filter(
    Q(title__icontains=q) |
    Q(overview__icontains=q) 
  ).order_by("-id")

  datasets_per_page = 10
  paginator = Paginator(datasets, datasets_per_page)

  # Get the current page number from the request's GET parameters
  page_number = request.GET.get('page')

  # Get the Page object for the current page
  page = paginator.get_page(page_number)
  return render(request, "base/home.html", {"page" : page, "q" : q})
  
  
def dataset(request, pk):
  current_dataset = Dataset.objects.get(id=pk)
  pks, scores = give_recommendations(current_dataset.id)
  similar_datasets = []
  # Primary Keys
  for pk in pks:
    similar_datasets.append(Dataset.objects.get(id=pk))
  return render(request, "base/dataset.html", {"dataset" : current_dataset, 
                                                "similar_datasets" : similar_datasets, 
                                                "scores" : scores, "pks" : pks})

  
# def upload(request):
#   # form = DatasetForm()
#   if request.method == "POST":
#     form = DatasetForm(request.POST, request.FILES)
#     if form.is_valid():
#       dataset = form.save()
#       categories = form.cleaned_data['category']
#       overview = f"{dataset.title} - {dataset.description} - {dataset.tags} - {', '.join([category.name for category in categories])}"
#       dataset.overview = overview
#       dataset.save()
#       return redirect("home")
#   else:
#     form = DatasetForm()
#   return render(request, "base/upload.html", {"form" : form})

def upload(request):
    if request.method == 'POST':
        form_first_page = DatasetFormFirstPage(request.POST)
        form_second_page = DatasetFormSecondPage(request.POST, request.FILES)

        if form_first_page.is_valid() and form_second_page.is_valid():
            dataset = form_first_page.save(commit=False)
            dataset.file = form_second_page.cleaned_data['file']
            dataset.save()
            return redirect('home')  # Replace 'success_page' with the actual URL for the success page
    else:
        form_first_page = DatasetFormFirstPage()
        form_second_page = DatasetFormSecondPage()

    return render(request, 'base/upload.html', {'form_first_page': form_first_page, 'form_second_page': form_second_page})


def download(request, pk):
  file = Dataset.objects.get(id=pk)
  response = HttpResponse(file.file, content_type='application/force-download')
  response['Content-Disposition'] = f'attachment; filename="{file.file.name}"'
  return response