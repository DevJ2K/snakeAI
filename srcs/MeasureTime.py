import time
from utils.Colors import *

class MeasureTime:
	def __init__(self, start: bool = False):
		self.t_start = None
		self.t_end = None
		if start == True:
			self.start()

	def __str__(self) -> str:
		if self.t_end is None:
			return "The timer is not ended."
		else:
			return f"Duration : {self.t_end // 1000000}ms"
	def start(self):
		self.t_start = time.perf_counter_ns()

	def stop(self, get_str: bool = False, duration_only: bool = False):
		if self.t_start is None:
			print("The timer has not started yet.")
		else:
			self.t_end = time.perf_counter_ns() - self.t_start
			self.t_start = None
			if duration_only:
				string_time = f"{self.t_end // 1000000}ms"
			else:
				string_time = f"{BHWHITE}Duration : {MAGB} {BHWHITE}{self.t_end // 1000000}ms {RESET}"
			if get_str:
				return string_time
			else:
				print(string_time)

if __name__ == "__main__":
	measureTime = MeasureTime()
	measureTime.start()
	time.sleep(0.12)
	measureTime.stop()
