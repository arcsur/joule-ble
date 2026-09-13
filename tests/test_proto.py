"""Tests for Joule protobuf messages and serialization."""

import pytest

from joule_ble.models import CookState, ErrorState, ProgramType, TurboCookState
from joule_ble.proto import joule_pb2


def test_circulator_data_point_serialization():
    """Test serializing and deserializing CirculatorDataPoint inside StreamMessage."""
    msg = joule_pb2.StreamMessage()
    dp = msg.circulatorDataPoint
    dp.bathTemp = 55.45
    dp.heaterTemp = 57.8
    dp.upperBoardTemp = 32.1
    dp.lowerBoardTemp = 30.5
    dp.motorRPM = 1150
    dp.heaterPWM = 80
    dp.timeRemaining = 1200
    dp.programStep = joule_pb2.COOK
    dp.errorState = joule_pb2.NO_ERROR
    dp.motorFaultFlag = 0

    serialized = msg.SerializeToString()
    assert len(serialized) > 0

    parsed = joule_pb2.StreamMessage()
    parsed.ParseFromString(serialized)
    assert parsed.HasField("circulatorDataPoint")
    p_dp = parsed.circulatorDataPoint
    assert pytest.approx(p_dp.bathTemp, 0.01) == 55.45
    assert pytest.approx(p_dp.heaterTemp, 0.01) == 57.8
    assert p_dp.motorRPM == 1150
    assert p_dp.programStep == joule_pb2.COOK
    assert p_dp.errorState == joule_pb2.NO_ERROR


def test_start_program_request():
    """Test serializing StartProgramRequest."""
    msg = joule_pb2.StreamMessage()
    req = msg.startProgramRequest
    prog = req.circulatorProgram
    prog.setPoint = 62.5
    prog.cookTime = 5400
    prog.programType = joule_pb2.MANUAL
    prog.delayedStart = 0
    prog.holdingTemperature = 0.0

    data = msg.SerializeToString()
    assert len(data) > 0

    parsed = joule_pb2.StreamMessage()
    parsed.ParseFromString(data)
    assert parsed.HasField("startProgramRequest")
    setpoint = parsed.startProgramRequest.circulatorProgram.setPoint
    assert pytest.approx(setpoint, 0.01) == 62.5
    assert parsed.startProgramRequest.circulatorProgram.cookTime == 5400


def test_identify_circulator_reply():
    """Test parsing IdentifyCirculatorReply."""
    msg = joule_pb2.StreamMessage()
    rep = msg.identifyCirculatorReply
    rep.name = "My Kitchen Joule"
    rep.serialNumber = "CS10001-998877"
    rep.firmwareVersion = "v1.9.3"
    rep.hardwareVersion = "v2.0"
    rep.modelNumber = "CS10001"

    raw = msg.SerializeToString()
    parsed = joule_pb2.StreamMessage()
    parsed.ParseFromString(raw)
    assert parsed.HasField("identifyCirculatorReply")
    assert parsed.identifyCirculatorReply.name == "My Kitchen Joule"
    assert parsed.identifyCirculatorReply.serialNumber == "CS10001-998877"


def test_model_enum_conversions():
    """Test enum conversion helpers."""
    assert CookState.from_proto(joule_pb2.COOK) == CookState.COOKING
    assert CookState.from_proto(joule_pb2.PRE_HEAT) == CookState.PRE_HEATING
    assert CookState.from_proto(joule_pb2.WAIT_FOR_FOOD) == CookState.WAITING_FOR_FOOD
    assert CookState.from_proto(9999) == CookState.UNKNOWN

    assert ProgramType.from_proto(joule_pb2.MANUAL) == ProgramType.MANUAL
    assert ProgramType.from_proto(joule_pb2.AUTOMATIC) == ProgramType.AUTOMATIC

    assert ErrorState.from_proto(joule_pb2.NO_ERROR) == ErrorState.NO_ERROR
    assert ErrorState.from_proto(joule_pb2.SOFT_ERROR) == ErrorState.SOFT_ERROR
    assert ErrorState.from_proto(joule_pb2.HARD_ERROR) == ErrorState.HARD_ERROR

    assert TurboCookState.from_proto(joule_pb2.NO_TURBO) == TurboCookState.NO_TURBO
    turbo_on = joule_pb2.TURBO_ENABLED
    assert TurboCookState.from_proto(turbo_on) == TurboCookState.TURBO_ENABLED
