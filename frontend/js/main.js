// Datum richtig formatieren
function formatDate(d) {
  return d.getDate() + "/" + d.getMonth() + "/" + d.getFullYear() + " " + d.getHours() + ":" + d.getMinutes()
}

// Main function
$(function() {
  t = document.getElementById('timeline')

  // Web Socket
  var ws = new WebSocket("ws://saturn.maschinen.space:8000");

  // Connection bestätigung
  ws.onopen = function(){
    console.log("Socket has been opened!");
  };

  // Nachrichten anzeigen
  ws.onmessage = function(message) {
    message = JSON.parse(message.data);
    console.log(message);
    var phret = message["guessed_party"].split("===JSON===")[1]
    guessment = JSON.parse(phret)
    console.log(guessment)
    var lastFac = ""
    var lastPro = 0.0
    for (var key in guessment)
      if (guessment[key] > lastPro)
      {
        lastPro = guessment[key]
        lastFac = key
      }
    guessed_faction = lastFac.replace("Die Linke", "linke")
                             .replace("Bündnis 90\\Die Grünen", "b90")
                             .replace("fraktionslos", "erica")

    var tweet = '<div class="tweet"><img src="' + message["profile_img"] + 
                '" class="tweet-avatar"><div class="tweet-political-real ' +
                 message["real_party"] + '">' + message["real_party"] +
                 '</div><div class="tweet-political-bot ' + guessed_faction +
                 '">' + guessed_faction + '</div><div class="tweet-content"><h1>' +
                 message["name"] + '</h1><h2>@' + message["handle"] + '</h2><p>' +
                 message["text"] + '</p><p class="timestamp">' +
                 formatDate(new Date(message["date"])) + '</p></div></div>';
    //console.log(guessment)
    $(tweet).prependTo($(".timeline")).hide().show("drop", 500);
  };
});

// smooth scroll
$(function() {
  $('a[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 1000);
        return false;
      }
    }
  });
});
