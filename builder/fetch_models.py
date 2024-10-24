from concurrent.futures import ThreadPoolExecutor
import whisperx

model_names = ["medium", "large-v1", "large-v2", "large-v3", "deepdml/faster-whisper-large-v3-turbo-ct2"]


def load_model(selected_model):
    '''
    Load and cache models in parallel
    '''
    for _attempt in range(5):
        while True:
            try:
                loaded_model = whisperx.load_model(selected_model, device="cpu", compute_type="int8")
            except (AttributeError, OSError):
                continue

            break

    return selected_model, loaded_model


models = {}

with ThreadPoolExecutor() as executor:
    for model_name, model in executor.map(load_model, model_names):
        if model_name is not None:
            models[model_name] = model