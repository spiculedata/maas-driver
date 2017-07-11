# Copyright 2017 Spicule LTD.  This software is licensed under the
# Apache 2.0 License.

"""Arduino Power Driver."""

__all__ = []

from provisioningserver.drivers.power import PowerDriver
from provisioningserver.logger import get_maas_logger
from provisioningserver.utils import shell
from twisted.internet.defer import maybeDeferred
import serial
import time

maaslog = get_maas_logger("drivers.power.wakeonlan")

REQUIRED_PACKAGES = []

class ArduinoPowerDriver(PowerDriver):

    name = 'arduino'
    description = "Arduino Power Driver."
    settings = []

    def detect_missing_packages(self):
        missing_packages = set()
        for binary, package in REQUIRED_PACKAGES:
            if not shell.has_command_available(binary):
                missing_packages.add(package)
        return list(missing_packages)

    def on(self, system_id, context):
        """Override `on` as we do not need retry logic."""
        return maybeDeferred(self.power_on, system_id, context)

    def off(self, system_id, context):
        """Override `off` as we do not need retry logic."""
        return maybeDeferred(self.power_off, system_id, context)

    def query(self, system_id, context):
        """Override `query` as we do not need retry logic."""
        return maybeDeferred(self.power_query, system_id, context)

    def power_on(self, system_id, context):
        """Power on machine using wake on lan."""
        ser = serial.Serial('/dev/ttyACM0',115200,timeout=1)
        ser.flushOutput()
        ser.write(chr(context.get("server_id")))
        ser.write(chr(1))
        r = ser.read(7)


    def power_off(self, system_id, context):
        """Power off machine manually."""
        ser = serial.Serial('/dev/ttyACM0',115200,timeout=1)
        ser.flushOutput()
        ser.write(chr(context.get("server_id")))
        ser.write(chr(1))
        r = ser.read(7)
 
    def power_query(self, system_id, context):
        """Power query machine manually."""
        maaslog.info(
            "You need to check power state of %s manually." % system_id)
        return 'unknown'


