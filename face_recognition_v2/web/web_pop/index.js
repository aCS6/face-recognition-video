function Minimize() {
    window.innerWidth = 100;
    window.innerHeight = 100;
    window.screenX = screen.width;
    window.screenY = screen.height;
    alwaysLowered = true;
  }

  function Maximize() {
    window.innerWidth = screen.width;
    window.innerHeight = screen.height;
    window.screenX = 0;
    window.screenY = 0;
    alwaysLowered = false;
  }

document.getElementById("min").addEventListener('click',Minimize )


document.addEventListener(
  "visibilitychange",
  function () {
    //console.log(document.hidden, document.visibilityState);

    if (document.hidden) {
      console.log("hidden");
      
    } else if (document.visibilityState) {
      console.log("Open");
    }
  },
  false
);
