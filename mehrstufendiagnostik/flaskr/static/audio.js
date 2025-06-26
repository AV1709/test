let record2 = document.querySelectorAll ('.record');

if (navigator.mediaDevices.getUserMedia) {
    //client is able to record audio
    /*
    let onMediaSetupSuccess = function (stream) {
        alert("Everything is working!")
    }
    */
    let onMediaSetupFailure = function(err) {
        for(var i = 0; i < record2.length; i++) {
            record2[i].disabled = true;
        }
        alert(err);
    }

    navigator.mediaDevices.getUserMedia({audio: true}).then(onMediaSetupSuccess, onMediaSetupFailure);

} else {
    alert('getUserMedia not supported in your browser');
}


function aufnehmen(element) {
            if (element.title !== 'disabled') {
                if (element.title == 'recording') {
                    element.title = 'not_recording';

                    fetch("/detect", {
                        method: "POST",
                        body: []
                    }).then((response) => response.json())
                        .then((data) => {
                            id = element.id
                            idd = id.replace('m','d')
                            iddesc = id.replace('m','_description')
                            fetch_textArea(idd, data.output2)
                            document.getElementById(iddesc).value=data.output2
                            textAreaAdjust(document.getElementById(iddesc))
                            element.src = '../static/microphone_off.svg'
                        })

                } else {
                    element.title = 'recording';
                    fetch("/record", {
                        method: "POST",
                        body: []
                    }).then((response) => {
                        element.src = '../static/microphone_on.svg'
                        })
                }
        }
}