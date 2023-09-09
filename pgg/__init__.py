from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'pgg'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ENDOWMENT = cu(20)
    MULTIPLIER = 3


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        p.endowment = C.ENDOWMENT


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()

class Player(BasePlayer):
    belief=models.CurrencyField(label='How much do you think the other participants ON AVERAGE will contribute?', min=0, max=C.ENDOWMENT)
    endowment = models.CurrencyField()
    contribution = models.CurrencyField(label='How much will you contribute?', min=0, max=C.ENDOWMENT)



# PAGES
class Decision(Page):
    form_model = 'player'
    form_fields = ['contribution', 'belief']



def set_payoffs(group: Group):
    num_players= len(group.get_players())
    group.total_contribution = sum([p.contribution for p in group.get_players()])
    group.individual_share = (group.total_contribution * C.MULTIPLIER) / num_players
    for p in group.get_players():

        p.payoff = p.endowment - p.contribution + group.individual_share


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    def vars_for_template(self):
        return {
            'contributions': [p.contribution for p in self.group.get_players()],
        }


page_sequence = [Decision, ResultsWaitPage, Results]
