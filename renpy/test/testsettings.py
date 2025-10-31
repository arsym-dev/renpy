# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from dataclasses import dataclass
import subprocess
import renpy

@dataclass
class TestReportSettings:
    hide_header: bool = False
    """Whether to hide the header at the start of the test run."""

    hide_execution: str = "no"
    """Whether to hide test execution output. One of 'no', 'hooks', 'testcases', or 'all'."""

    hide_summary: bool = False
    """Whether to hide the summary at the end of the test run."""

    report_detailed: bool = False
    """Whether to report detailed information about each test case."""

    report_skipped: bool = False
    """
    Whether to include skipped test cases in the summary.
    Requires 'report_detailed' to be True to have any effect.
    """


@dataclass
class TestSettings:
    enable_all: bool = False
    """Set all test cases to enabled, ignoring their enabled flag."""

    focus_trials: int = 100
    """The number of times to try to find a mouse focus before giving up."""

    force: bool = False
    """Force the test to proceed despite suppress_underlay"""

    git_revision: str = ""
    """The git revision of the current source tree, if available."""

    maximum_framerate: bool = True
    """Use the maximum framerate (unlocked framerate) during tests."""

    overwrite_screenshots: bool = False
    """Whether to overwrite existing screenshots. If True, no comparison is done."""

    screenshot_directory: str = "tests/screenshots"
    """The directory to store screenshots in."""

    timeout: float = 5.0
    """The number of seconds to wait for a test to complete before failing it."""

    timeout_multiplier: float | None = None
    """
    A multiplier applied to timeouts to account for slow systems.
    If None, it is computed automatically at the start of the test run.
    """

    transition_timeout: float = 5.0
    """The number of seconds to wait for a transition to complete before skipping it."""

    report = TestReportSettings()

    def __post_init__(self) -> None:
        if not self.git_revision:
            try:
                self.git_revision = subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True
                ).strip()
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass

    @property
    def adjusted_timeout(self) -> float:
        """
        The number of seconds to wait for a test to complete before failing it.
        Includes timeout multiplier.
        """

        if self.timeout_multiplier is None:
            return self.timeout
        return self.timeout * self.timeout_multiplier

    def compute_timeout_multiplier(self) -> None:
        """
        Compute the timeout multiplier based on the system's performance.
        Give more time to slower systems.

        Bypassed if timeout_multiplier is already set.
        """
        if self.timeout_multiplier is not None:
            return

        refresh_rate = renpy.exports.get_refresh_rate()
        frame_times = renpy.display.interface.frame_times

        if len(frame_times) < 5:
            fps = refresh_rate
        else:
            ift = [ (j - i) for i, j in zip(frame_times, frame_times[1:]) ]
            frame_interval = sum(ift[-10:])/10.0
            if frame_interval == 0:
                fps = refresh_rate
            else:
                fps = 1.0 / frame_interval

        self.timeout_multiplier = max(1, min(refresh_rate / fps, 3))
        if self.timeout_multiplier > 1.0:
            renpy.test.testreporter.reporter.log_message(
                f"Adjusting timeouts by factor of {self.timeout_multiplier:.2f}"
                f" (fps: {fps:.2f}, refresh rate: {refresh_rate})")


_test = TestSettings()
