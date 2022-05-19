/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

package mozilla.telemetry.glean.private

import androidx.annotation.VisibleForTesting
import mozilla.telemetry.glean.internal.DatetimeMetric
import mozilla.telemetry.glean.utils.calendarToDatetime
import java.util.Calendar
import java.util.Date
import java.util.concurrent.TimeUnit as AndroidTimeUnit

/**
 * This implements the developer facing API for recording datetime metrics.
 *
 * Instances of this class type are automatically generated by the parsers at build time,
 * allowing developers to record values that were previously registered in the metrics.yaml file.
 */
class DatetimeMetricType(meta: CommonMetricData, timeUnit: TimeUnit = TimeUnit.MINUTE) {
    val inner = DatetimeMetric(meta, timeUnit)

    /**
     * Set a datetime value, truncating it to the metric's resolution.
     *
     * @param value The [Date] value to set. If not provided, will record the current time.
     */
    fun set(value: Date = Date()) {
        val cal = Calendar.getInstance()
        cal.time = value
        set(cal)
    }

    /**
     * Set a datetime value, truncating it to the metric's resolution.
     *
     * This is provided as an internal-only function for convenience and so that we can
     * test that timezones are passed through correctly.  The normal public interface uses
     * [Date] objects which are always in the local timezone.
     *
     * @param value The [Calendar] value to set. If not provided, will record the current time.
     */
    internal fun set(cal: Calendar) {
        val dt = calendarToDatetime(cal)
        inner.set(dt)
    }

    @VisibleForTesting(otherwise = VisibleForTesting.NONE)
    @JvmOverloads
    fun testGetValue(pingName: String? = null): Date? {
        return inner.testGetValue(pingName)?.let { dt ->
            val cal = Calendar.getInstance()
            cal.set(Calendar.ZONE_OFFSET, AndroidTimeUnit.SECONDS.toMillis(dt.offsetSeconds.toLong()).toInt())
            cal.set(Calendar.DST_OFFSET, 0) // we pretend its never DST. The zone offset will have that already.
            cal.set(Calendar.YEAR, dt.year.toInt())
            cal.set(Calendar.MONTH, dt.month.toInt() - 1) // java.util.calendar's month is 0-based for months
            cal.set(Calendar.DAY_OF_MONTH, dt.day.toInt())
            cal.set(Calendar.HOUR_OF_DAY, dt.hour.toInt())
            cal.set(Calendar.MINUTE, dt.minute.toInt())
            cal.set(Calendar.SECOND, dt.second.toInt())
            cal.set(Calendar.MILLISECOND, AndroidTimeUnit.NANOSECONDS.toMillis(dt.nanosecond.toLong()).toInt())
            cal.getTime()
        }
    }

    @VisibleForTesting(otherwise = VisibleForTesting.NONE)
    @JvmOverloads
    fun testGetValueAsString(pingName: String? = null): String? {
        return inner.testGetValueAsString(pingName)
    }

    @VisibleForTesting(otherwise = VisibleForTesting.NONE)
    @JvmOverloads
    fun testHasValue(pingName: String? = null): Boolean {
        return inner.testGetValue(pingName) != null
    }
}
