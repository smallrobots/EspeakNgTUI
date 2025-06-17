from dataclasses import dataclass
import shlex

@dataclass
class EspeakParameters:
    text: str = ""
    voice: str = ""
    speed: str = "175"
    pitch: str = "50"
    volume: str = "100"
    word_gap: str = "0"


def compose_command(params: EspeakParameters) -> str:
    """Return the espeak-ng command string for the given parameters."""
    cmd = ["espeak-ng"]
    if params.voice:
        cmd.extend(["-v", params.voice])
    if params.speed:
        cmd.extend(["-s", params.speed])
    if params.pitch:
        cmd.extend(["-p", params.pitch])
    if params.volume:
        cmd.extend(["-a", params.volume])
    if params.word_gap:
        cmd.extend(["-g", params.word_gap])
    if params.text:
        cmd.append(shlex.quote(params.text))
    return " ".join(cmd)
