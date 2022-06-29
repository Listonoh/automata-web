import json

# import logging

from restarting_automata import BaseAutomaton

# from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .forms import InputAutomata, InputInt, InputWord, InputLogLevel
from .models import Automata

from rest_framework.views import APIView  
from django.http import JsonResponse  

class HomeView(APIView):  
    def get(self, request, format=None):
        return JsonResponse({"message":
        'HELLO WORLD FROM DJANGO AND DOCKER'})  

def index(request):
    a = "something"
    return render(request, "automata_pages/result.html", {"automaton_result": a})


def computed_result(request):
    text = request.POST["word"]
    defin = request.POST["automata"]
    a = BaseAutomaton()
    a.load(json.loads(defin))
    correct = a.evaluate(text)
    return automata_form(request, False, True, True, json.dumps(a.definition), correct)


def automata_form(
    request,
    error=False,
    AutomatonParsed=False,
    hasAutomaton=False,
    automat=None,
    result=None,
    word="",
):
    inputAutomata = InputAutomata()
    inputWord = InputWord()
    if "error" in request.GET:
        error = True
    return render(
        request,
        "automata_pages/new_automata.html",
        {
            "InputAutomata": inputAutomata,
            "InputWord": inputWord,
            "error": error,
            "AutomatonParsed": AutomatonParsed,
            "hasAutomaton": hasAutomaton,
            "Automat": automat,
            "result": result,
            "word": word,
        },
    )


def create_automat_from_form(request):
    # form = InputAutomata(request.POST, request.FILES)
    au = BaseAutomaton()
    if request.FILES:
        a = request.FILES["file"]
        b = json.load(a)
        au.load(b)
    else:
        au.definition = json.loads(request.POST["text"])

    return automata_form(request, False, True, True, json.dumps(au.definition))


def saved_automatas(reqest):
    automats = Automata.objects.order_by("-published_date")
    context = {"list_of_automats": automats}
    return render(reqest, "automata_pages/saved_automata.html", context)


def playground(reqest, automat_id):
    automat = get_object_or_404(Automata, pk=automat_id)
    context = {
        "automat": automat,
        "log_level": InputLogLevel(),
        "automat_id": automat_id,
        "InputWord": InputWord(),
    }
    return render(reqest, "automata_pages/playground.html", context)


def input(request):
    if request.method == "POST":
        if "SubmitAutomaton" in request.POST:
            return create_automat_from_form(request)
        if "SubmitWord" in request.POST:
            return computed_result(request)
    else:
        return automata_form(request)


def result(request, automat_id):
    if request.method == "POST":
        try:
            automat = Automata.objects.get(pk=automat_id)
            text = request.POST["word"]
            log_level = 0
            if request.POST["log_level"] in ["result", "cycles", "instructions"]:
                log_level = ["result", "cycles", "instructions"].index(
                    request.POST["log_level"])
            a = BaseAutomaton(out_mode=log_level)
            a.load(automat.json_specification)
            correct = a.evaluate(text)
            context = {"automaton_result": correct, "logs": a.logs.split("\n")}
            return render(request, "automata_pages/result.html", context)
        except KeyError:
            raise Http404("Automat can not be loaded " + automat_id)
        # except:
        #     raise Http404("Automat does not exist " + request.POST["word"])
    else:
        raise Http404("no post method")
