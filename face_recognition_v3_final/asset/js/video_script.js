// Getting the dom
let camera_button = document.querySelector("#start-camera");
let video = document.querySelector("#video");

// Varibale Declaration
let camera_stream = null;
let media_recorder = null;
let blobs_recorded = [];

// stop both mic and camera after finishing the exam
function stopBothVideoAndAudio(stream) {
  stream.getTracks().forEach(function (track) {
    if (track.readyState == "live") {
      track.stop();
    }
  });
}

// First appearance
camera_button.addEventListener("click", async function () {
  camera_button.style.display = "none";
  camera_stream = await navigator.mediaDevices.getUserMedia({
    video: true,
    audio: true,
  });
  video.srcObject = camera_stream;

  // set MIME type of recording as video/webm
  media_recorder = new MediaRecorder(camera_stream, { mimeType: "video/webm" });

  // event : new recorded video blob available
  media_recorder.addEventListener("dataavailable", function (e) {
    blobs_recorded.push(e.data);
  });

  // event : recording stopped & all blobs sent
  media_recorder.addEventListener("stop", function () {
    // Take the recorded blob file
    var blobvid = new Blob(blobs_recorded, { type: "video/webm" });
    var formData = new FormData();
    formData.append("vid", blobvid);
    document.getElementById("demo").style.color = "blue";
    document.getElementById("demo").style.display = "block";
    document.getElementById("demo").innerHTML =
      "Please wait a moment.. You're being recognised!";
    // call ajax
    $.ajax({
      type: "POST",
      url: "video_handler.php",
      data: formData,
      cache: false,
      contentType: false,
      processData: false,
      success: function (data) {
        if (data) {
          flaskCall(data);
        }
      },
    });
    // stop camera and mic
    stopBothVideoAndAudio(camera_stream);
    video.style.display = "none";
  });
  // start recording with each recorded blob having 1 second video
  media_recorder.start(1000);

  var recording_time = 2000; // 2 seconds video taking
  setTimeout(function () {
    media_recorder.stop();
  }, recording_time);
});

function flaskCall(data) {
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:7500/home/" + data,
    cache: false,
    contentType: false,
    processData: false,
    success: function (data1, data2) {
      if (data1 == "Unknown") {
        document.getElementById("demo").innerHTML =
          "You aren't recognised ! Login Failed !";
        document.getElementById("demo").style.color = "red";
      } else if (data1 == "Failed") {
        document.getElementById("demo").innerHTML = "Login Failed";
        document.getElementById("demo").style.color = "red";
      } else {
        document.getElementById("demo").innerHTML =
          data1 + ", Your login success";
        document.getElementById("demo").style.color = "green";
        document.getElementById("demo").style.textAlign = "center";
      }
    },
  });
}
