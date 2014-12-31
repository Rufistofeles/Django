from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader, Template
from django.core.urlresolvers import reverse
from django.views import generic
from pyfirmata import Arduino

from polls.models import Choice, Poll

class IndexView(generic.ListView):

	template_name = 'polls/index.html'
	context_object_name = 'latest_poll_list'
	
	def get_queryset(self):
		return Poll.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):

	model = Poll
	
	template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):

	model = Poll
	
	template_name = 'polls/results.html'

class Results2View(generic.DetailView):

	model = Poll
	
	template_name = 'polls/results2.html'

	
def vote(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'poll': p,
			'error_message': "No seleccionaste una opcion.",
		})

	else:
		selected_choice.votes += 1
		selected_choice.save()
		
		
		#a = Arduino('/dev/ttyACM0')
		if selected_choice.id == 1:
			#a.digital[13].write(1)
			return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
		else:
			#a.digital[13].write(0)
			return HttpResponseRedirect(reverse('polls:results2', args=(p.id,)))
		


