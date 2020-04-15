# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from typing import List, Optional


from .. import _ffi
from .._dispatcher import Dispatcher
from ..testing import ErrorType
from .. import _util


from .lifetime import Lifetime
from .timeunit import TimeUnit


class TimespanMetricType:
    """
    This implements the developer facing API for recording timespan metrics.

    Instances of this class type are automatically generated by
    `glean.load_metrics`, allowing developers to record values that were
    previously registered in the metrics.yaml file.

    The timespan API exposes the `TimespanMetricType.start`,
    `TimespanMetricType.stop` and `TimespanMetricType.cancel` methods.
    """

    def __init__(
        self,
        disabled: bool,
        category: str,
        lifetime: Lifetime,
        name: str,
        send_in_pings: List[str],
        time_unit: TimeUnit,
    ):
        self._disabled = disabled
        self._send_in_pings = send_in_pings

        self._handle = _ffi.lib.glean_new_timespan_metric(
            _ffi.ffi_encode_string(category),
            _ffi.ffi_encode_string(name),
            _ffi.ffi_encode_vec_string(send_in_pings),
            len(send_in_pings),
            lifetime.value,
            disabled,
            time_unit.value,
        )

    def __del__(self):
        if getattr(self, "_handle", 0) != 0:
            _ffi.lib.glean_destroy_timespan_metric(self._handle)

    def start(self):
        """
        Start tracking time for the provided metric.

        This records an error if it’s already tracking time (i.e. `start` was
        already called with no corresponding `stop`): in that case the original
        start time will be preserved.
        """
        if self._disabled:
            return

        start_time = _util.time_ns()

        @Dispatcher.launch
        def start():
            _ffi.lib.glean_timespan_set_start(self._handle, start_time)

    def stop(self):
        """
        Stop tracking time for the provided metric.

        Sets the metric to the elapsed time, but does not overwrite an already
        existing value.
        This will record an error if no `start` was called or there is an already
        existing value.
        """
        if self._disabled:
            return

        stop_time = _util.time_ns()

        @Dispatcher.launch
        def stop():
            _ffi.lib.glean_timespan_set_stop(self._handle, stop_time)

    def cancel(self):
        """
        Abort a previous `start` call. No error is recorded if no `start` was called.
        """
        if self._disabled:
            return

        @Dispatcher.launch
        def cancel():
            _ffi.lib.glean_timespan_cancel(self._handle)

    def set_raw_nanos(self, elapsed_nanos: int):
        """
        Explicitly set the timespan value, in nanoseconds.

        This API should only be used if your library or application requires recording
        times in a way that can not make use of [start]/[stop]/[cancel].

        [setRawNanos] does not overwrite a running timer or an already existing value.

        Args:
            elapsed_nanos (int): The elapsed time to record, in nanoseconds.
        """
        if self._disabled:
            return

        @Dispatcher.launch
        def set_raw_nanos():
            _ffi.lib.glean_timespan_set_raw_nanos(self._handle, elapsed_nanos)

    def test_has_value(self, ping_name: Optional[str] = None) -> bool:
        """
        Tests whether a value is stored for the metric for testing purposes
        only.

        Args:
            ping_name (str): (default: first value in send_in_pings) The name
                of the ping to retrieve the metric for.

        Returns:
            has_value (bool): True if the metric value exists.
        """
        if ping_name is None:
            ping_name = self._send_in_pings[0]

        return bool(
            _ffi.lib.glean_timespan_test_has_value(
                self._handle, _ffi.ffi_encode_string(ping_name)
            )
        )

    def test_get_value(self, ping_name: Optional[str] = None) -> int:
        """
        Returns the stored value for testing purposes only.

        Args:
            ping_name (str): (default: first value in send_in_pings) The name
                of the ping to retrieve the metric for.

        Returns:
            value (bool): value of the stored metric.
        """
        if ping_name is None:
            ping_name = self._send_in_pings[0]

        if not self.test_has_value(ping_name):
            raise ValueError("metric has no value")

        return _ffi.lib.glean_timespan_test_get_value(
            self._handle, _ffi.ffi_encode_string(ping_name)
        )

    def test_get_num_recorded_errors(
        self, error_type: ErrorType, ping_name: Optional[str] = None
    ) -> int:
        """
        Returns the number of errors recorded for the given metric.

        Args:
            error_type (ErrorType): The type of error recorded.
            ping_name (str): (default: first value in send_in_pings) The name
                of the ping to retrieve the metric for.

        Returns:
            num_errors (int): The number of errors recorded for the metric for
                the given error type.
        """
        if ping_name is None:
            ping_name = self._send_in_pings[0]

        return _ffi.lib.glean_timespan_test_get_num_recorded_errors(
            self._handle, error_type.value, _ffi.ffi_encode_string(ping_name),
        )


__all__ = ["TimespanMetricType"]
