// Función para leer una cookie por nombre
function getCookie(name) {
    const value = "; " + document.cookie;
    const parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
    return "";
  }
  
  // Función para establecer una cookie con una duración en días
  function setCookie(name, value, days) {
    var expires = "";
    if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
  }
  
  // Se asigna el evento a cada enlace en la lista
  document.addEventListener("DOMContentLoaded", function() {
    var links = document.querySelectorAll("#js-links a");
    links.forEach(function(link) {
      link.addEventListener("click", function(e) {
        e.preventDefault();
        var linkHref = link.getAttribute("href");
        // Recupera la cookie "visited" y la convierte en array
        var visited = getCookie("visited");
        var visitedArray = visited ? visited.split(",") : [];
        // Si el enlace no se encuentra, se añade
        if (visitedArray.indexOf(linkHref) === -1) {
          visitedArray.push(linkHref);
        }
        // Se actualiza la cookie "visited" con una duración de 30 días
        setCookie("visited", visitedArray.join(","), 30);
        // Redirige al destino
        window.location.href = linkHref;
      });
    });
  });
  