let camera_button = document.querySelector("#start-camera");
let video = document.querySelector("#video");
let start_button = document.querySelector("#start-record");
let stop_button = document.querySelector("#stop-record");
let download_link = document.querySelector("#download-video");

let camera_stream = null;
let media_recorder = null;
let blobs_recorded = [];

// stop both mic and camera
function stopBothVideoAndAudio(stream) {
  stream.getTracks().forEach(function (track) {
    if (track.readyState == "live") {
      track.stop();
    }
  });
}

camera_button.addEventListener("click", async function () {
  start_button.style.display = "block";

  camera_button.style.display = "none";

  camera_stream = await navigator.mediaDevices.getUserMedia({
    video: true,
    audio: true,
  });
  video.srcObject = camera_stream;
});

start_button.addEventListener("click", function () {
  start_button.style.display = "none";
  stop_button.style.display = "block";
  // set MIME type of recording as video/webm
  media_recorder = new MediaRecorder(camera_stream, { mimeType: "video/webm" });
  console.log(media_recorder);
  // event : new recorded video blob available
  media_recorder.addEventListener("dataavailable", function (e) {
    blobs_recorded.push(e.data);
  });
  console.log("After Recording ");
  // event : recording stopped & all blobs sent
  media_recorder.addEventListener("stop", function () {
    console.log("stop2");
    // create local object URL from the recorded video blobs
    let video_local = URL.createObjectURL(
      new Blob(blobs_recorded, { type: "video/webm" })
    );
    download_link.href = video_local;
    //console.log(blobs_recorded);
    console.log(download_link);
    download_link.click();

    var blobvid = new Blob(blobs_recorded, { type: "video/webm" });
    var formData = new FormData();
    formData.append("vid", blobvid);

    var request = new XMLHttpRequest();
    request.open("POST", a.php);
    request.send(formData);

    stopBothVideoAndAudio(camera_stream);
    video.style.display = "none";
  });

  console.log("Before 1000");
  // start recording with each recorded blob having 1 second video
  media_recorder.start(1000);
});

stop_button.addEventListener("click", function () {
  console.log("Stop click 1");
  media_recorder.stop();
});
