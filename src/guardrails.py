from llm_guard.input_scanners import PromptInjection
from llm_guard.input_scanners.prompt_injection import MatchType

input_guard = PromptInjection(threshold=0.92, match_type=MatchType.FULL, use_onnx=True)
