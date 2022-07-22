from django.shortcuts import render, HttpResponseRedirect
# from django.http import HttpResponse
from .models import UpdateList
from .forms import EmployeeList

# Create your views here.


def index(response, id):
	ls = UpdateList.objects.get(id=id)
	if response.method == 'POST':
		if response.POST.get("save"):
			for item in ls.item_set.all():
				if response.POST.get("c" + str(item.id)) == "clicked":
					item.complete = True
				else:
					item.complete = False
				item.save()
		elif response.POST.get("newItem"):
			txt = response.POST.get("new")
			if len(txt) > 2:
				ls.item_set.create(text=txt, complete=False)
			else:
				print("Invalid input")
			ls.save()
	return render(response, "webapp/list.html", {"ls": ls})


def show(response):
	ls = UpdateList.objects.all()
	if response.method == 'GET':
		return render(response, "webapp/show.html", {"ls": ls})


def home(response):
	return render(response, "webapp/home.html", {})


def create(response):
	if response.method == 'POST':
		form = EmployeeList(response.POST)

		if form.is_valid():
			n = form.cleaned_data['name']
			u = UpdateList(name=n)
			u.save()
		return HttpResponseRedirect("/show/%i" % u.id)
	else:
		form = EmployeeList()
	return render(response, "webapp/create.html", {"form": form})


# def delete(response):
# 	if response.method == 'POST':
