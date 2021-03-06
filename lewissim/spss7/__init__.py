from collections import OrderedDict

from lewis.adapters.epics import PV, EpicsInterface
from lewis.core.statemachine import State
from lewis.devices import Device

from epics import caput, caget


def r_select_impl(pitch, mask):
    return mask >> int(pitch - 1) & 0b1


def select_impl(pitch, value, mask):
    mask |= (0b1 << pitch - 1)
    value ^= mask
    return value, mask


def zero_mask(pitch, mask):
    return mask ^ (0b1 << pitch - 1)


def selected_impl(pitch, values):
    return (values >> int(pitch - 1)) & 0b1




class SimulatedSps(Device):
    _fine_adjustment1 = 0
    _fine_adjustment2 = 0
    _fa_select1 = 0
    _fa_select2 = 0
    _values = 0b0
    _mask = 0b0
    move = 0

    def __init__(self):
        for i in range(1, 37):
            for param in ['_select', '_selected', 'selectable',
                          'park_position', 'alarm']:
                setattr(self, '%s_%d' % (param, i), 0)
        for i in range(1, 37):
            setattr(self, '%s_%d' % ('selectable', i), i >= 18)
        super(SimulatedSps, self).__init__()
        self.cmd = ''

    ###################

    @property
    def selected_1(self):
        return selected_impl(1, self._values)

    @property
    def select_1(self):
        return r_select_impl(1, self._mask)

    @select_1.setter
    def select_1(self, value):
        self._select_impl(1, value)

    @property
    def selected_2(self):
        return selected_impl(2, self._values)

    @property
    def select_2(self):
        return r_select_impl(2, self._mask)

    @select_2.setter
    def select_2(self, value):
        self._select_impl(2, value)

    @property
    def selected_3(self):
        return selected_impl(3, self._values)

    @property
    def select_3(self):
        return r_select_impl(3, self._mask)

    @select_3.setter
    def select_3(self, value):
        self._select_impl(3, value)

    @property
    def selected_4(self):
        return selected_impl(4, self._values)

    @property
    def select_4(self):
        return r_select_impl(4, self._mask)

    @select_4.setter
    def select_4(self, value):
        self._select_impl(4, value)

    @property
    def selected_5(self):
        return selected_impl(5, self._values)

    @property
    def select_5(self):
        return r_select_impl(5, self._mask)

    @select_5.setter
    def select_5(self, value):
        self._select_impl(5, value)

    @property
    def selected_6(self):
        return selected_impl(6, self._values)

    @property
    def select_6(self):
        return r_select_impl(6, self._mask)

    @select_6.setter
    def select_6(self, value):
        self._select_impl(6, value)

    @property
    def selected_7(self):
        return selected_impl(7, self._values)

    @property
    def select_7(self):
        return r_select_impl(7, self._mask)

    @select_7.setter
    def select_7(self, value):
        self._select_impl(7, value)

    @property
    def selected_8(self):
        return selected_impl(8, self._values)

    @property
    def select_8(self):
        return r_select_impl(8, self._mask)

    @select_8.setter
    def select_8(self, value):
        self._select_impl(8, value)

    @property
    def selected_9(self):
        return selected_impl(9, self._values)

    @property
    def select_9(self):
        return r_select_impl(9, self._mask)

    @select_9.setter
    def select_9(self, value):
        self._select_impl(9, value)

    @property
    def selected_10(self):
        return selected_impl(10, self._values)

    @property
    def select_10(self):
        return r_select_impl(10, self._mask)

    @select_10.setter
    def select_10(self, value):
        self._select_impl(10, value)

    @property
    def selected_11(self):
        return selected_impl(11, self._values)

    @property
    def select_11(self):
        return r_select_impl(11, self._mask)

    @select_11.setter
    def select_11(self, value):
        self._select_impl(11, value)

    @property
    def selected_12(self):
        return selected_impl(12, self._values)

    @property
    def select_12(self):
        return r_select_impl(12, self._mask)

    @select_12.setter
    def select_12(self, value):
        self._select_impl(12, value)

    @property
    def selected_13(self):
        return selected_impl(13, self._values)

    @property
    def select_13(self):
        return r_select_impl(13, self._mask)

    @select_13.setter
    def select_13(self, value):
        self._select_impl(13, value)

    @property
    def selected_14(self):
        return selected_impl(14, self._values)

    @property
    def select_14(self):
        return r_select_impl(14, self._mask)

    @select_14.setter
    def select_14(self, value):
        self._select_impl(14, value)

    @property
    def selected_15(self):
        return selected_impl(15, self._values)

    @property
    def select_15(self):
        return r_select_impl(15, self._mask)

    @select_15.setter
    def select_15(self, value):
        self._select_impl(15, value)

    @property
    def selected_16(self):
        return selected_impl(16, self._values)

    @property
    def select_16(self):
        return r_select_impl(16, self._mask)

    @select_16.setter
    def select_16(self, value):
        self._select_impl(16, value)

    @property
    def selected_17(self):
        return selected_impl(17, self._values)

    @property
    def select_17(self):
        return r_select_impl(17, self._mask)

    @select_17.setter
    def select_17(self, value):
        self._select_impl(17, value)

    @property
    def selected_18(self):
        return selected_impl(18, self._values)

    @property
    def select_18(self):
        return r_select_impl(18, self._mask)

    @select_18.setter
    def select_18(self, value):
        self._select_impl(18, value)

    @property
    def selected_19(self):
        return selected_impl(19, self._values)

    @property
    def select_19(self):
        return r_select_impl(19, self._mask)

    @select_19.setter
    def select_19(self, value):
        self._select_impl(19, value)

    @property
    def selected_20(self):
        return selected_impl(20, self._values)

    @property
    def select_20(self):
        return r_select_impl(20, self._mask)

    @select_20.setter
    def select_20(self, value):
        self._select_impl(20, value)

    @property
    def selected_21(self):
        return selected_impl(21, self._values)

    @property
    def select_21(self):
        return r_select_impl(21, self._mask)

    @select_21.setter
    def select_21(self, value):
        self._select_impl(21, value)

    @property
    def selected_22(self):
        return selected_impl(22, self._values)

    @property
    def select_22(self):
        return r_select_impl(22, self._mask)

    @select_22.setter
    def select_22(self, value):
        self._select_impl(22, value)

    @property
    def selected_23(self):
        return selected_impl(23, self._values)

    @property
    def select_23(self):
        return r_select_impl(23, self._mask)

    @select_23.setter
    def select_23(self, value):
        self._select_impl(23, value)

    @property
    def selected_24(self):
        return selected_impl(24, self._values)

    @property
    def select_24(self):
        return r_select_impl(24, self._mask)

    @select_24.setter
    def select_24(self, value):
        self._select_impl(24, value)

    @property
    def selected_25(self):
        return selected_impl(25, self._values)

    @property
    def select_25(self):
        return r_select_impl(25, self._mask)

    @select_25.setter
    def select_25(self, value):
        self._select_impl(25, value)

    @property
    def selected_26(self):
        return selected_impl(26, self._values)

    @property
    def select_26(self):
        return r_select_impl(26, self._mask)

    @select_26.setter
    def select_26(self, value):
        self._select_impl(26, value)

    @property
    def selected_27(self):
        return selected_impl(27, self._values)

    @property
    def select_27(self):
        return r_select_impl(27, self._mask)

    @select_27.setter
    def select_27(self, value):
        self._select_impl(27, value)

    @property
    def selected_28(self):
        return selected_impl(28, self._values)

    @property
    def select_28(self):
        return r_select_impl(28, self._mask)

    @select_28.setter
    def select_28(self, value):
        self._select_impl(28, value)

    @property
    def selected_29(self):
        return selected_impl(29, self._values)

    @property
    def select_29(self):
        return r_select_impl(29, self._mask)

    @select_29.setter
    def select_29(self, value):
        self._select_impl(29, value)

    @property
    def selected_30(self):
        return selected_impl(30, self._values)

    @property
    def select_30(self):
        return r_select_impl(30, self._mask)

    @select_30.setter
    def select_30(self, value):
        self._select_impl(30, value)

    @property
    def selected_31(self):
        return selected_impl(31, self._values)

    @property
    def select_31(self):
        return r_select_impl(31, self._mask)

    @select_31.setter
    def select_31(self, value):
        self._select_impl(31, value)

    @property
    def selected_32(self):
        return selected_impl(32, self._values)

    @property
    def select_32(self):
        return r_select_impl(32, self._mask)

    @select_32.setter
    def select_32(self, value):
        self._select_impl(32, value)

    @property
    def selected_33(self):
        return selected_impl(33, self._values)

    @property
    def select_33(self):
        return r_select_impl(33, self._mask)

    @select_33.setter
    def select_33(self, value):
        self._select_impl(33, value)

    @property
    def selected_34(self):
        return selected_impl(34, self._values)

    @property
    def select_34(self):
        return r_select_impl(34, self._mask)

    @select_34.setter
    def select_34(self, value):
        self._select_impl(34, value)

    @property
    def selected_35(self):
        return selected_impl(35, self._values)

    @property
    def select_35(self):
        return r_select_impl(35, self._mask)

    @select_35.setter
    def select_35(self, value):
        self._select_impl(35, value)

    @property
    def selected_36(self):
        return selected_impl(36, self._values)

    @property
    def select_36(self):
        return r_select_impl(36, self._mask)

    @select_36.setter
    def select_36(self, value):
        self._select_impl(36, value)

    ##################

    def _select_impl(self, pitch, value):
        if value:
            self._values, self._mask = select_impl(pitch, self._values, self._mask)
        else:
            self._mask = zero_mask(pitch, self._mask)

    @property
    def fa_read1(self):
        return self._fine_adjustment1

    @property
    def fa_read2(self):
        return self._fine_adjustment2

    @property
    def fa_select1(self):
        return self._fine_adjustment1

    @fa_select1.setter
    def fa_select1(self, value):
        self._fa_select1 = 1 if value else 0
        self._fine_adjustment1 ^= self._fa_select1

    @property
    def fa_select2(self):
        return self._fine_adjustment2

    @fa_select2.setter
    def fa_select2(self, value):
        self._fa_select2 = 1 if value else 0
        self._fine_adjustment2 ^= self._fa_select2

    # debug
    def _find_pitch(self):
        for p in range(36):
            print('pitch%d: %r' % (p + 1, self._values >> p & 0b1))
        print('')

    def _get_state_handlers(self):
        return {
            'idle': State(),
            }

    def _get_initial_state(self):
        return 'idle'

    def _get_transition_handlers(self):
        return OrderedDict()

    @property
    def aout(self):
        return self.cmd

    @aout.setter
    def aout(self, command):
        if command == 'P850=3':
            parking_position=caget('SQ:AMOR:SEL2:MIRROR.HLM')
            caput('SQ:AMOR:SEL2:MIRROR.VAL', parking_position)

    @property
    def ainp(self):
        return ''


def pitch_pvs(pitchid):
    x = {
        ':P%d:Select' % pitchid: PV('select_%d' % pitchid, read_only=False,
                                   doc='Select pitch', type='int'),
        ':P%d:Selectable' % pitchid: PV('selectable_%d' % pitchid, type='int',
                                       read_only=True, doc='Pitch can be '
                                                           'selected'),
        ':P%d:Selected' % pitchid: PV('selected_%d' % pitchid, type='int',
                                     read_only=True, doc='Pitch is selected'),
        ':P%d:ParkPosition' % pitchid: PV('park_position_%d' % pitchid,
                                         doc='Pitch is parked', type='int',
                                         read_only=True),
        ':P%d:Alarm' % pitchid: PV('alarm_%d' % pitchid, read_only=True,
                                  type='int')
        }
    return x


class SpsS7EpicsInterface(EpicsInterface):
    pvs = {
        ':MCU1:FineAdjustment:Select': PV('fa_select1',
                                    doc='Enable fine adjustment of the '
                                        'mirrors', type='int'),
        ':MCU2:FineAdjustment:Select': PV('fa_select2',
                                    doc='Enable fine adjustment of the '
                                        'mirrors', type='int'),
        ':MCU1:FineAdjustment:Selected': PV('fa_read1',
                                          doc='Fine adjustment selected',
                                          read_only=True, type='int'),
        ':MCU2:FineAdjustment:Selected': PV('fa_read2',
                                          doc='Fine adjustment selected',
                                          read_only=True, type='int'),
        ':MCU2:Move': PV('move', doc='NOT WORKING -- Motor is moving',
                        read_only=True, type='int'),
        ':MCU1:Move': PV('move', doc='NOT WORKING -- Motor is moving',
                        read_only=True, type='int'),
        '.AOUT': PV('aout', doc='Direct connection to EPICS asyn Octet',
                   type='string'),
        '.AINP': PV('ainp', doc='Readback from EPICS asyn Octet',
                   type='string'),
        }
    for pid in range(1, 37):
        pvs.update(pitch_pvs(pid))

    _commands = {
        'start': 'start', 'stop': 'stop',
        }

    _last_command = ''

    @property
    def execute_command(self):
        """
        Command to execute. Possible commands are start, stop.
        """
        return ''

    @execute_command.setter
    def execute_command(self):
        command = self._commands.get(value)

        getattr(self.device, command)()
        self._last_command = command

    @property
    def last_command(self):
        """
        The last command that was executed successfully.
        """
        return self._last_command


setups = dict(
    sps=dict(device_type=SimulatedSps, parameters=dict(override_initial_data={
        'selectable_33': 1, 'selectable_34': 1, 'selectable_35': 1,
        'selectable_36': 1,

        })))

framework_version = '1.2.1'
