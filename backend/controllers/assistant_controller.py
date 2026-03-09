class AssistantController:
    def __init__(self, stt, llm):

        self.stt = stt
        self.llm = llm

    def process_voice(self):

        audio_file = self.stt.record_audio()

        text = self.stt.transcribe(audio_file)

        print("User:", text)

        response = self.llm.generate(text)

        return response
