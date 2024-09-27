from django.shortcuts import render
from django.views.generic import ListView, DetailView

from sending.models import Sending


class SendingListView(ListView):
    model = Sending


class SendingDetailView(DetailView):
    model = Sending


