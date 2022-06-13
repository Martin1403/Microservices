import click
from stt.api.tests import async_run, AsyncTest
from stt.api.model import DeepSpeech

from pydub import AudioSegment


@click.command("test-async")
@async_run
async def test_async():
    async with AsyncTest() as test:
        async_object = await test
    click.echo(async_object.text)


@click.command("test-model")
@async_run
async def test_model():
    audio_segment = AudioSegment.from_wav(file="stt/static/audio/test.wav")
    model_path, scorer_path = "stt/model/output_graph.tflite", "stt/model/output_graph.scorer"
    model = DeepSpeech(model_path=model_path, scorer_path=scorer_path)
    text = model.stt(audio_segment.get_array_of_samples())
    click.echo(text)
