from parchmint import Device
from parchmint.component import Component
from parchmint.connection import Connection
from parchmint.device import ValveType
from parchmint.feature import Feature
from parchmint.layer import Layer
import pytest
from parchmint.target import Target


@pytest.fixture
def temp_device():
    device = Device()
    device.name = "dev1"
    device.xspan = 100000
    device.yspan = 50000

    return device


def test_get_connections_for_edge(temp_device, layer_dict, component_dict):
    temp_device.add_layer(Layer(json_data=layer_dict))
    component1 = Component(json_data=component_dict, device_ref=temp_device)
    temp_device.add_component(component1)
    component2 = Component(json_data=component_dict, device_ref=temp_device)
    component2.ID = "c2"
    component2.name = "c2"
    temp_device.add_component(component2)

    connection1 = Connection(device_ref=temp_device)
    connection1.ID = "connection1"
    source_target = Target()
    source_target.component = component1.ID
    source_target.port = "1"
    connection1.source = source_target

    sink_target = Target()
    sink_target.component = component2.ID
    sink_target.port = "1"
    connection1.sinks.append(sink_target)

    temp_device.add_connection(connection1)

    connection2 = Connection(device_ref=temp_device)
    connection2.ID = "connection2"
    source_target = Target()
    source_target.component = component1.ID
    source_target.port = "2"
    connection2.source = source_target

    sink_target = Target()
    sink_target.component = component2.ID
    sink_target.port = "2"
    connection2.sinks.append(sink_target)

    temp_device.add_connection(connection2)

    assert temp_device.get_connections_for_edge(component1, component2) == [
        connection1,
        connection2,
    ]

    assert temp_device.get_connections_for_edge(component2, component1) == []


def test_to_parchmint_v1_x(
    device_dict,
    connection_dict,
    component_dict,
    layer_dict,
    feature_dict,
    valve1_dict,
    valve2_dict,
):
    device = Device()
    device.name = "dev1"
    device.xspan = 100000
    device.yspan = 50000
    device.add_layer(Layer(json_data=layer_dict))
    device.add_feature(Feature(json_data=feature_dict, device_ref=device))
    device.add_component(Component(json_data=component_dict, device_ref=device))
    valve1 = Component(json_data=valve1_dict, device_ref=device)
    valve2 = Component(json_data=valve2_dict, device_ref=device)
    device.add_component(valve1)
    device.add_component(valve2)
    con1 = Connection(json_data=connection_dict, device_ref=device)
    device.add_connection(con1)
    device.map_valve(valve1, con1, ValveType.NORMALLY_OPEN)
    device.map_valve(valve2, con1, ValveType.NORMALLY_CLOSED)
    assert device.to_parchmint_v1_x() == device_dict
