import logging

from django.http import Http404
from django.shortcuts import render_to_response
from gibbs import concentration_profile
from gibbs import reaction
from gibbs import reaction_form


_REACTION_TEMPLATES_BY_SUBMIT = {'Update': 'reaction_page.html',
                                 'Save': 'print_reaction.html'}


def ReactionPage(request):    
    """Renders a page for a particular reaction."""
    form = reaction_form.ReactionForm(request.GET)
    if not form.is_valid():
        logging.error(form.errors)
        raise Http404
    
    # Figure out which template to render (based on which submit button they pressed).
    print form.cleaned_submit
    template_name = _REACTION_TEMPLATES_BY_SUBMIT.get(form.cleaned_submit,
                                                      'reaction_page.html')

    rxn = reaction.Reaction.FromForm(form)
    query = form.cleaned_query
    if form.cleaned_reactionId:
        query = rxn.GetQueryString()
    if form.cleaned_submit == 'Reverse':
        rxn.SwapSides()
        query = rxn.GetQueryString()
    if form.cleaned_balance_w_water:
        rxn.TryBalanceWithWater()
        query = rxn.GetQueryString()
    if form.cleaned_balance_electrons:
        rxn.BalanceElectrons()
        query = rxn.GetQueryString()
    if form.cleaned_replace_co2:
        rxn.TryReplaceCO2()
        query = rxn.GetQueryString()
    
    logging.error(rxn)
    
    # Render the template.
    balance_with_water_link = rxn.GetBalanceWithWaterLink(query)
    balance_electrons_link = rxn.GetBalanceElectronsLink(query)
    replace_co2_link = rxn.GetReplaceCO2Link(query)
    template_data = {'reaction': rxn,
                     'query': query,
                     'ph': rxn.ph,
                     'pmg': rxn.pmg,
                     'ionic_strength': rxn.i_s,
                     'concentration_profile': str(rxn.concentration_profile),
                     'balance_with_water_link': balance_with_water_link,
                     'balance_electrons_link': balance_electrons_link,
                     'replace_co2_link': replace_co2_link}
    return render_to_response(template_name, template_data)