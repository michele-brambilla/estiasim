from time import sleep

from transitions import Machine, State


attocube_states = [
    'system idle',
    State(
        name='measurement starting', on_enter=['on_enter_measurement_starting']
    ),
    State(
        name='measurement running', on_enter=['on_enter_measurement_running']
    ),
    State(
        name='optics alignment starting',
        on_enter=['on_enter_alignment_starting'],
    ),
    State(
        name='optics alignment running',
        on_enter=['on_enter_alignment_running'],
    ),
    'pilot laser enabled',
]

attocube_transitions = [
    {'trigger': 'measure', 'source': 'system idle', 'dest': 'measurement '
                                                         'starting'},
    {
        'trigger': 'align',
        'source': 'pilot laser enabled',
        'dest': 'optics alignment starting',
    },
    {
        'trigger': 'disable_laser',
        'source': 'pilot laser enabled',
        'dest': 'system idle',
    },
    {
        'trigger': 'enable_laser',
        'source': 'system idle',
        'dest': 'pilot laser enabled',
    },
    {'trigger': 'stop', 'source': '*', 'dest': 'system idle'},
]


class NarcolepticAttocube(object):

    # Define some states. Most of the time, narcoleptic superheroes are just like
    # everyone else. Except for...

    def __init__(self, name):
        self.name = name

        # Initialize the state machine
        self.machine = Machine(
            model=self,
            states=attocube_states,
            transitions=attocube_transitions,
            initial='system idle',
            ignore_invalid_triggers=True,
        )

        self.machine.add_ordered_transitions(
            ['measurement starting', 'measurement running', 'system idle']
        )

        self.machine.add_ordered_transitions(
            [
                'pilot laser enabled',
                'optics alignment starting',
                'optics alignment running',
                'pilot laser enabled',
            ]
        )

    def on_enter_measurement_starting(self):
        sleep(1)
        self.next_state()

    def on_enter_measurement_running(self):
        sleep(3)
        self.next_state()

    def on_enter_alignment_starting(self):
        print(self.state)
        sleep(1)
        self.next_state()

    def on_enter_alignment_running(self):
        print(self.state)
        sleep(3)
        self.next_state()
