import sys
import tty
import termios
from typing import Iterable

class ManualAutoCompleter:
    def __init__(self, candidates: Iterable[str]):
        self.commands = sorted(set(candidates))
        self._pending_matches = None
        self._pending_buffer = ""

    def read_line(self, prompt: str = "$ ") -> str:
        fd = sys.stdin.fileno()
        old_attrs = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            sys.stdout.write(prompt)
            sys.stdout.flush()
            buffer = ""
            while True:
                ch = sys.stdin.read(1)
                if ch == "\t":
                        inserted = self._handle_completion(buffer)
                        buffer += inserted
                        sys.stdout.write(inserted)
                        sys.stdout.flush()
                elif ch in ("\n", "\r"):
                    sys.stdout.write("\n")
                    return buffer
                elif ch == "\x7f":
                    if buffer:
                        buffer = buffer[:-1]
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                else:
                    buffer += ch
                    sys.stdout.write(ch)
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_attrs)

    def _handle_completion(self, buffer: str) -> str:
        if self._pending_matches and buffer == self._pending_buffer:
            self._print_matches(self._pending_matches, buffer)
            self._pending_matches = None
            return ""

        matches = [cmd for cmd in self.commands if cmd.startswith(buffer)]
        if buffer != self._pending_buffer:
            self._pending_matches = None
        if not matches:
            self._bell()
            return ""
        endings = [cmd[len(buffer):] for cmd in matches]
        if len(matches) == 1:
            return endings[0] + " " if endings[0] and not endings[0].endswith(" ") else endings[0]
        lcp = self._longest_common_prefix(endings)
        if lcp:
            self._pending_matches = None
            return lcp
        self._pending_matches = matches
        self._pending_buffer = buffer
        self._bell()
        return ""

    def _print_matches(self, matches: Iterable[str], buffer: str) -> None:
        sys.stdout.write("\n")
        sys.stdout.write("  ".join(matches))
        sys.stdout.write("\n")
        sys.stdout.write("$ ")
        sys.stdout.write(buffer)
        sys.stdout.flush()

    def _bell(self) -> None:
        sys.stdout.write("\x07")
        sys.stdout.flush()

    @staticmethod
    def _longest_common_prefix(strs: Iterable[str]) -> str:
        if not strs:
            return ""
        reference = strs[0]
        for i, c in enumerate(reference):
            for other in strs[1:]:
                if i >= len(other) or other[i] != c:
                    return reference[:i]
        return reference
