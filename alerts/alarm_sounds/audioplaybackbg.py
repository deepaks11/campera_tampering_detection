import os
import time
import pyaudio
import wave
import threading
from processor.logger import trace, exc
import warnings
warnings.filterwarnings(action='ignore')
root = os.getcwd()


# Audio background playback class (wav format is supported)
class AudioPlaybackBg:
    def __init__(self, wavfile: str, audio_data):  # audio = pyaudio object
        try:
            with wave.open(wavfile, 'rb') as wav:
                if wav.getsampwidth() != 2:  # Checking bits/sampling (bytes/sampling)
                    raise RuntimeError("wav file {} does not have int16 format".format(wavfile))
                if wav.getframerate() != 16000:  # Checking sampling rate
                    raise RuntimeError("wav file {} does not have 16kHz sampling rate".format(wavfile))
                self.wav_data = wav.readframes(wav.getnframes())

            self.lock = threading.Lock()
            self.thread = threading.Thread(target=self.play_thread)
            self.exit_flag = False
            self.play_flag = False
            self.play_buf = None  # Current playback buffer
            self.audio = audio_data  # PyAudio object
            self.frame_size = 2048  # Audio frame size (samples / frame)
            self.sampling_rate = 16000  # Audio sampling rate
            self.playback_stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=self.sampling_rate,
                                                   output=True,
                                                   frames_per_buffer=self.frame_size)
            self.thread.start()
        except Exception as e:
            exc.exception('error occurred in pyaudio object {}'.format(e))

    def __del__(self):
        try:
            self.terminate_thread()
        except Exception as e:
            exc.exception('error occurred in del function of audio playback bg {}'.format(e))

    def terminate_thread(self):
        try:
            self.exit_flag = True
            self.thread.join()
        except Exception as e:
            exc.exception('error occurred in terminate thread {}'.format(e))

    def play_thread(self):
        try:
            while self.exit_flag is False:
                if self.play_flag is False:
                    time.sleep(0.1)
                    continue
                if self.play_buf is None:
                    self.play_buf = self.wav_data[:]
                # Cut out an audio frame from the playback buffer
                if len(self.play_buf) > self.frame_size * 2:
                    play_data = self.play_buf[:self.frame_size * 2]
                    self.play_buf = self.play_buf[self.frame_size * 2:]
                else:
                    play_data = (self.play_buf + b'\0\0' * self.frame_size)[:self.frame_size * 2]
                    self.lock.acquire()
                    self.play_flag = False
                    self.lock.release()
                    self.play_buf = None
                # Playback an audio frame
                self.playback_stream.write(frames=play_data, num_frames=self.frame_size)
                time.sleep(0.1)  # 16KHz, 2048samples = 128ms. Wait must be shorter than 128ms.
        except Exception as e:
            exc.exception('error occurred in play thread {}'.format(e))

    def play(self):
        try:
            self.lock.acquire()
            self.play_flag = True
            self.lock.release()
        except Exception as e:
            exc.exception('error occurred in play audio playback class {}'.format(e))

    def stop(self):
        try:
            self.play_buf = None
            self.lock.acquire()
            self.play_flag = False
            self.lock.release()
        except Exception as e:
            exc.exception('error occurred in stop {}'.format(e))

# def audio_music(audio_type, wav_dir):
#     try:
#
#         trace.info('Starting sound alarm')
#         audio = pyaudio.PyAudio()
#         # wav_dir = './alerts/alarm_sounds/'
#         # sound_thread_thankyou = audio_playback_bg(wav_dir + 'thankyou.wav', audio)
#         # sound_thread_welcome = audio_playback_bg(wav_dir + 'welcome.wav', audio)
#         sound_thread_warning = audio_playback_bg(wav_dir + 'warning.wav', audio)
#
#         if audio_type:
#             sound_thread_warning.play()
#
#         else:
#             sound_thread_warning.stop()
#
#     except Exception as ex:
#         exc.exception('Failed to start sound alarm{}'.format(ex))
#
#
# def alarm_sound(path):
#     try:
#         audio_music(True, path)
#         time.sleep(5)
#         audio_music(False, path)
#     except Exception as ex:
#         exc.exception('Failed to start alarm sound {}'.format(ex))


try:
    trace.info('Starting sound alarm for Trespass Detection ..')

    audio = pyaudio.PyAudio()
    wav_dir = root + '/alerts/alarm_sounds/'
    sound_thread_thankyou = AudioPlaybackBg(wav_dir + 'thankyou.wav', audio)
    sound_thread_welcome = AudioPlaybackBg(wav_dir + 'welcome.wav', audio)
    sound_thread_warning = AudioPlaybackBg(wav_dir + 'warning.wav', audio)

except Exception as ex:
    exc.exception('Failed to start sound alarm for Trespass Detection {}'.format(ex))


def alarm_sd():
    sound_thread_warning.play()
    time.sleep(5)
    sound_thread_warning.stop()
    