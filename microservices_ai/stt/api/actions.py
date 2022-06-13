import base64
from functools import wraps
import os
import sys

from pydub import AudioSegment

from stt.api.model import DeepSpeech


model_path = "stt/model/output_graph.tflite"
scorer_path = "stt/model/output_graph.scorer"
model = DeepSpeech(model_path=model_path if os.path.exists(model_path) else sys.exit(1),
                   scorer_path=scorer_path if os.path.exists(scorer_path) else None)


def action_endpoint(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        # Get data from endpoint
        data = await f(*args, **kwargs)
        # Encode data from string to bytes
        data = base64.decodebytes(data.data.encode('ascii'))
        # Make audio segment for manipulate with data
        audio_segment = AudioSegment(data, frame_rate=16000, sample_width=2, channels=1)
        # Get array from segment
        np_audio = audio_segment[100:].get_array_of_samples()
        # Convert array if samples to text
        text = model.stt(np_audio)
        return {"data": text}
    return decorated_function
