import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import (
  CONF_ID, CONF_MAC_ADDRESS
)
from . import (
    bthome_ns, BTHome, CONF_BTHome_ID
)

DEPENDENCIES = ["bthome"]

CONF_MAC_ADDRESS = "mac_address"
CONF_MEASUREMENT_TYPE = "measurement_type"

MEASUREMENT_TYPES_BINARY_SENSOR = {
    "generic_boolean": 0x0F,
    "power": 0x10,
    "opening": 0x11,
    "battery": 0x15,
    "battery_charging": 0x16,
    "carbon_monoxide": 0x17,
    "cold": 0x18,
    "connectivity": 0x19,
    "door": 0x1A,
    "garage_door": 0x1B,
    "gas": 0x1C,
    "heat": 0x1D,
    "light": 0x1E,
    "lock": 0x1F,
    "moisture": 0x20,
    "motion": 0x21,
    "moving": 0x22,
    "occupancy": 0x23,
    "plug": 0x24,
    "presence": 0x25,
    "problem": 0x26,
    "running": 0x27,
    "safety": 0x28,
    "smoke": 0x29,
    "sound": 0x2A,
    "tamper": 0x2B,
    "vibration": 0x2C,
    "window": 0x2D,
}

def _lookup_measurement_type(value):
  if value in MEASUREMENT_TYPES_BINARY_SENSOR:
    return MEASUREMENT_TYPES_BINARY_SENSOR[value]
  raise cv.Invalid(f"Cannot resolve measurement type '{value}'.")

def _translate_measurement_type(value):
    if isinstance(value, int):
        return value
    try:
        return int(value)
    except ValueError:
        pass
    return _lookup_measurement_type(value)

def validate_measurement_type(value):
    value = _translate_measurement_type(value)
    ## todo check min/max
    return value

BTHomeBinarySensor = bthome_ns.class_("BTHomeBinarySensor", binary_sensor.BinarySensor, cg.Component)

def validate_config(config):
    # todo: sould not allow binary_sensor if receiver_pin is not registered
    return config

CONFIG_SCHEMA = cv.All(
    binary_sensor.BINARY_SENSOR_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(BTHomeBinarySensor),
        cv.GenerateID(CONF_BTHome_ID): cv.use_id(BTHome),
        cv.Required(CONF_MAC_ADDRESS): cv.mac_address,
        cv.Required(CONF_MEASUREMENT_TYPE): validate_measurement_type,
    }), 
    validate_config,
)

async def to_code(config):
    bthome_component = await cg.get_variable(config[CONF_BTHome_ID])

    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await binary_sensor.register_binary_sensor(var, config)

    cg.add(var.set_address(config[CONF_MAC_ADDRESS].as_hex))
    cg.add(var.set_measurement_type(config[CONF_MEASUREMENT_TYPE]))
    
    cg.add(bthome_component.register_sensor(var))