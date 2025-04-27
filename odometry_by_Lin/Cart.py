import time

class RobotTimeController:
    """
    A Unity-style fixed-step loop with three stages:
      1. Awake()  - run once at start-up, blocking everything else
      2. Fixed_Update / Update  - executed at a fixed time interval (fixed_dt)
      3. Last_Update – idle buffer between intervals (wait / lag handling)

    Parameters
    ----------
    fixed_dt : float
        The target timestep in seconds (e.g. 0.01 -> 100 Hz).
    awake_cb : callable or None
        A user-supplied function executed once during construction
        (hardware init, parameter loading, etc.). Code blocks here
        until the callback finishes.
    """
    # -------------------------------------------------------------- #
    def __init__(self, fixed_dt: float = 0.01, awake_cb=None):
        self.fixed_dt = fixed_dt
        self.awake_cb = awake_cb

        # ------Awake phase (runs once, blocks everything else)----- #
        self._awake_done = False
        self._run_awake() # ---blocks until Awake completes--------- #

        # ------Timing initialisation (starts AFTER Awake)---------- #
        self._interval_start = time.time()
        self._next_interval  = self._interval_start + self.fixed_dt

        # Runtime info
        self._timestamps: dict[str, float] = {}
        self.sync_status: str = "ontime"   # "ontime" | "wait" | "lag"

    # =============================================================== #
    #  Fixed‑timestep control                                         #
    # =============================================================== #
    def fixed_update(self) -> bool:
        if not self._awake_done:
            return False                        # Awake not done → skip

        now = time.time()

        # Interval reached or passed?
        if now >= self._next_interval:
            missed = int((now - self._interval_start) // self.fixed_dt)

            if missed > 0:                     # we missed ≥1 slot → lag
                self.sync_status = "lag"
                self._interval_start += missed * self.fixed_dt
            else:                              # on time
                self.sync_status = "ontime"
                self._interval_start = self._next_interval

            self._next_interval = self._interval_start + self.fixed_dt
            self._timestamps = {"start": self._interval_start}
            return True

        # Not time yet
        return False

    # -------------------------------------------------------------- #
    def update(self):
        if not self._awake_done:
            return

        self.update_sensor();   self._timestamps["sensor"]  = time.time()
        self.update_odometry(); self._timestamps["odometry"]= time.time()
        self.update_motor();    self._timestamps["motor"]   = time.time()
        self.upload_status();   self._timestamps["status"]  = time.time()

        # If we finished early → wait until next interval
        if self._timestamps["status"] < self._next_interval:
            self.sync_status = "wait"

    # -------------------------------------------------------------- #
    def last_update(self):
        """
        Runs continuously between intervals.
        • If status == "wait" : sleep until the *next* interval begins.
        • If status == "lag"  : sleep until the interval AFTER the missed one.
        • If status == "ontime": nothing special.
        """
        if not self._awake_done:
            return

        if self.sync_status == "wait":
            time.sleep(max(0.0, self._next_interval - time.time()))

        elif self.sync_status == "lag":
            next_slot = self._interval_start + self.fixed_dt
            time.sleep(max(0.0, next_slot - time.time()))

        # ontime → no sleep, loop continues immediately

    def update_sensor(self):   pass
    def update_odometry(self): pass
    def update_motor(self):    pass
    def upload_status(self):   pass


    # ============================================================= #
    #  --------------------- helpers ------------------------------ #
    # ============================================================= #
    def _run_awake(self):
        """Internal: execute the user‑supplied awake callback once."""
        if self.awake_cb is not None:
            self.awake_cb()            # blocks here until finished
        self._awake_done = True

    # ---------------- getters ---------------- #
    def get_timestamps(self) -> dict[str, float]:
        """Return a *copy* of the time stamps for the last interval."""
        return self._timestamps.copy()

    def get_sync_status(self) -> str:
        """Current sync status: 'wait', 'lag', or 'ontime'."""
        return self.sync_status
