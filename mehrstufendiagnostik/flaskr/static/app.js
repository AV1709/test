
function update_demo(output){
    document.getElementById("demo").innerHTML = '<b>Befund: </b><br> '
    let j = 1
    for (let i = 1; i < 89; i++) {
        let stri = (i*10).toString()+'out'
        let strir = (i*10+1).toString()+'out'
        if (output[stri]) {
            document.getElementById("demo").innerHTML += ' ' + output[stri];
        }
        if (output[strir]) {
            document.getElementById("demo").innerHTML += ' ' + output[strir];
        }
    }
    if (output['e3out']) {
        document.getElementById('e3t').value = output['e3out'];
        document.getElementById("demo").innerHTML += ' ' + output['e3out'];
    }
    if (output['e4out']) {
        document.getElementById('e4t').value = output['e4out'];
        document.getElementById("demo").innerHTML += ' ' + output['e4out'];
    }
}


function fetch_radio(name, value) {
    let formData = new FormData();
    formData.append("name", name);
    formData.append("value", value);

    fetch("/process", {
        method: "POST",
        body: formData
    }).then((response) => response.json())
    .then((data) => {
        update_demo(data.output)
    })

    if (value==="unnotice") {
        document.getElementById(name+"_notice_left").checked=false;
        document.getElementById(name+"_description").disabled=true;
        document.getElementById(name+"_description").value='';
        document.getElementById(name+"m").title='disabled';
        document.getElementById(name+"m").style.opacity='0.5';
        document.getElementById(String(Number(name)+1)+"_notice_right").checked=false;
        document.getElementById(String(Number(name)+1)+"_description").disabled=true;
        document.getElementById(String(Number(name)+1)+"_description").value='';
        document.getElementById(String(Number(name)+1)+"m").title='disabled';
        document.getElementById(String(Number(name)+1)+"m").style.opacity='0.5';
    } else if (value === "notice_left") {
        document.getElementById(name+"_description").disabled=false;
        document.getElementById(name+"m").title='not_recording';
        document.getElementById(name+"m").style.opacity='1';
    } else if (value === "notice_right") {
        document.getElementById(name+"_description").disabled=false;
        document.getElementById(name+"m").title='not_recording';
        document.getElementById(name+"m").style.opacity='1';
    }
}

function fetch_checkbox(name, value) {
    let formData = new FormData();
    formData.append("name", name);
    formData.append("value", value);

    fetch("/process", {
        method: "POST",
        body: formData
    }).then((response) => response.json())
    .then((data) => {
        update_demo(data.output)
    })

    document.getElementById(name+"_description").disabled=false;
    document.getElementById(name+"m").title='not_recording';
        document.getElementById(name+"m").style.opacity='1';
    var regex = /\d+/g;
    var matches = name.match(regex);
    if (matches % 10 == 1) {
    matches = matches-1
    }
    document.getElementById(matches+"_unnotice").checked=false;
}

function fetch_textArea(name, value) {
    let formData = new FormData();
    formData.append("name", name);
    formData.append("value", value);

    fetch("/process", {
        method: "POST",
        body: formData
    }).then((response) => response.json())
    .then((data) => {
        update_demo(data.output)
    })
}



function textAreaAdjust(element) {
  element.style.height = "1px";
  element.style.height = (element.scrollHeight)+"px";
}


function load(data,out,file_path){
    for (item in data) {
        val = data[item]
        if (item === 'e3' || item === 'e4') {
            document.getElementById(item+'t').value = val;
        } else {
            if (val === 'unnotice') {
                document.getElementById(item+'_unnotice').checked = "true";
            } else if (val ==='notice_left' || val ==='notice_right') {
                document.getElementById(item+'_'+val).checked = "true"; //('10_notice_left' or '10_notice_right')
                document.getElementById(item+'_description').disabled = false;
            } else {
                if (item % 10 === 1) { // 331-> notice_right
                    document.getElementById(item+'_notice_right').checked = "true";
                } else { //330 -> notice_left
                    document.getElementById(item+'_notice_left').checked = "true";
                }
                document.getElementById(item+'_description').disabled = false;
                document.getElementById(item+"_description").value = val;
                textAreaAdjust(document.getElementById(item+"_description"));
            }
        }
    }
    if (file_path != "") {
        document.getElementById("save-path").innerHTML = "<b>Gespeichert unter: " + file_path +'</b>';
    }
    update_demo(out)

}