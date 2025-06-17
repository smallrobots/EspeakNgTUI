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
    args = ["espeak-ng"]
    if params.voice:
        args += ["-v", params.voice]
    if params.speed:
        args += ["-s", params.speed]
    if params.pitch:
        args += ["-p", params.pitch]
    if params.volume:
        args += ["-a", params.volume]
    if params.word_gap:
        args += ["-g", params.word_gap]
    if params.text:
        args.append(shlex.quote(params.text))  # 👈 protezione da caratteri strani
    retValue = " ".join(args)
    return retValue
