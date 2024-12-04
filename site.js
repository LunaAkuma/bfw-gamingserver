"use strict"; // Aktiviert den strict mode

const video = document.getElementById("backgroundVideoXXX");

let isPlayingBackward = false;

// Funktion zur Steuerung der Wiedergabe
const playVideo = () => {
  if (isPlayingBackward) {
    // Rückwärts abspielen
    if (video.currentTime <= 0) {
      // Wenn das Video den Anfang erreicht hat, wechseln wir in den Vorwärtsmodus
      isPlayingBackward = false;
      video.currentTime = 0; // Starten beim Anfang
    } else {
      video.currentTime -= 0.0005; // Gehe zurück in moderaten Schritten
    }
  } else {
    // Vorwärts abspielen
    if (video.currentTime >= video.duration - 1) {
      // Wenn das Video das Ende erreicht, wechseln wir in den Rückwärtsmodus
      isPlayingBackward = true;
      video.currentTime = video.duration; // Starten am Ende
    } else {
      video.currentTime += 0.0005; // Gehe vorwärts in moderaten Schritten
    }
  }

  // Erneut die Funktion mit requestAnimationFrame aufrufen
  requestAnimationFrame(playVideo);
};

// Startet das Video und startet die Schleife
video.play();
requestAnimationFrame(playVideo); // Startet die Animation
