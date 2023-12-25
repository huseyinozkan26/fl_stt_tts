$(document).ready(function () {
	let gumStream;
	let rec;
	let input;
	let audioContext;

	$('#recordButton').on('mousedown', startRecording);
	$('#recordButton').on('mouseup', function(){
		setTimeout(function(){
			stopRecording()
		},1000)
	});

	function startRecording() {
		$("#result_container").html("Kaydediliyor...")
		console.log("recordButton clicked");
		let constraints = { audio: true, video: false };

		navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
			console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

			audioContext = new (window.AudioContext || window.webkitAudioContext)();
			$('#formats').html("Format: 1 channel pcm @ " + audioContext.sampleRate / 1000 + "kHz");

			gumStream = stream;
			input = audioContext.createMediaStreamSource(stream);

			rec = new Recorder(input, { numChannels: 1 });
			rec.record();

			console.log("Recording started");
		}).catch(function (err) {

		});
	}

	function stopRecording() {
		rec.stop();
		gumStream.getAudioTracks()[0].stop();
		rec.exportWAV(createFileForSubmit);
		console.log("recording stop");
		$("#result_container").html("Kayıt durdu.")
	}

	function createFileForSubmit(blob) {
		const formData = new FormData();
                formData.append('audio', blob, 'recorded.wav');
                formData.append('correct_text', document.getElementById('correct_text').value);
				$("#result_container").html("Değerlendirme yapılıyor...")
                $.ajax({
                    type: 'POST',
                    url: 'http://localhost:8000/stt/api/speech-recognition/',
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function (response) {
                        console.log('Server response:', response);
						$("#result_container").html("Puan: "+ response.accuracy+ "Metin: "+response.text);
                    },
                    error: function (error) {
                        console.error('Error sending recording to server:', error.responseText);
                    }
                });
	}


});