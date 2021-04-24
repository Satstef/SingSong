/* Funzioni JS per il form di aggiornamento canzoni */

// Collegato a "onsubmit" del form aggiornamento serve per validare il form da frontend,
// senza dover ricaricare la pagina
function validateForm() {
  // variabili associate a field del form di update
  var titolo = document.forms["update"]["titolo"].value;
  var artista = document.forms["update"]["artista"].value;
  var album = document.forms["update"]["album"].value;
  var genere = document.forms["update"]["genere"].value;
  var titolo = titolo.trim();

  // Se il field titolo canzone è vuoto richiama un errore
  if (titolo == "") {
    alert("Song title required");
    return false;
  }

  /* Prima di passare i dati aggiornati al backend vedo se l'utente ha inserito i
  dati corretti (nome canzone, album e artista già esistenti sollevano un errore).
  La lista delle canzoni ricevuta in JS da Python è una lista di tuple, dove ogni tupla
  è una canzone con il suo album, artista ecc. Cerco quindi la tupla corrispondente
  alla canzone inserita dall'utente.
  Come prima cosa ricavo solo la lista dei titoli delle canzoni presenti.
  variabile:data è la lista ricevuta da Python. Vedi HTML.*/
  titoli = [];
  for (x = 0; x < data.length; x++) {
    // inserisco in lista solo il primo elemento di ogni tupla
    titoli.push(data[x][0]);
  }

  /* Confronto il titolo inserito dall'utente con i titoli presenti nella lista "titoli"
  Se il titolo inserito dall'utente è nella lista dei titoli, prendo l'indice numerico.
  La posizione del titolo nella lista corrisponde alla posizione della tupla nella lista
  di tuple. Quindi l'indice mi servirà per recuperare la lista del titolo, album, artista
  genere di quella canzone. */
  var check = titoli.includes(titolo);
  if (check == true) {
    var ind = titoli.indexOf(titolo);
    // data[ind] è l'array in cui si trovano: titolo, album, artista associati.
    var song_data = data[ind];

    /* Accertato che il titolo inserito già c'è, confronto anche l'album e l'artista inseriti
    dall'utente. Se (e solo se) sia l'album che l'artista si trovano nell'array del titolo
    viene sollevato un errore poichè è inutile fare una modifica dalla canzone */
    var alb = song_data.includes(album);
    var art = song_data.includes(artista);
    var gen = song_data.includes(genere);
    if (alb == true && art == true && gen == true) {
      alert("The song title already exists and is associated with \
                the album and artist you entered.");
      return false;
    }else {
      return
    }

  // se il titolo inserito dall'utente non è presente allora manda i dati a Python.
  }else {
    return
  }
}


// Funzione non utilizzata. Solo un esempio...
function send_song() {
  var myform = new FormData();
  myform.append('tito', 'giorgio');
  myform.append("marco", "3456");
  //var obj = ["macchina", "capo"]
  //var obj = {"casa":"fine", "corsa":"dorme"};
  //document.getElementById('demo').innerHTML = form.get('tito');
  //formData.append("albu", album);
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("POST", "{{ url_for('profile.update_song', nome=current_user.nome)}}", true); // false for synchronous request
  xmlHttp.setRequestHeader("Content-type", "multipart/form-data");
  xmlHttp.send(myform);
  alert("Titolo già");
  return
}


// Questa funzione permette di far comparire il form di aggiornamento, compilato
// con i dati della corrispondente riga della tabella.
function visualizza(id){
  // Recupero la query string dell'URL con l'hashtag
  var str = window.location.hash;
  // elimino l'hashtag
  const queryString = str.slice(1);
  // URLSearchParams serve per ottenere i valori delle chiavi nella queryString
  const urlParams = new URLSearchParams(queryString);
  const titolo = urlParams.get('tito');
  const album = urlParams.get('albu');
  const artista = urlParams.get('arti');
  const genere = urlParams.get('gene');
  const idtit = urlParams.get('n');
  document.getElementById("u_tit").value = titolo;
  document.getElementById("u_tit_id").value = idtit;
  document.getElementById("u_alb").value = album;
  document.getElementById("u_alb_hide").value = album;
  document.getElementById("u_art").value = artista;
  document.getElementById("u_art_hide").value = artista;
  document.getElementById("u_gen").value = genere;
  document.getElementById("u_gen_hide").value = genere;
  if (document.getElementById){
    if(document.getElementById(id).style.display == 'none'){
      document.getElementById(id).style.display = 'block';
    }
  }
}

function closeForm(id) {
  document.getElementById(id).style.display = 'none';
}

/* La funzione JS per ordinare alfabeticamente le colonne della lista canzoni */

function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("Mytable");
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc";
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}
